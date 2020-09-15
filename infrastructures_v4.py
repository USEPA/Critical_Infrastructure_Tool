# -*- coding: utf-8 -*-
"""
infrastructures_v4.py
Created on Sun Oct 23 19:23:05 2018
Created by: Mitchell Wendt
Revised: 08/28/2019
Revised by: Mitchell Wendt
"""

#import statements
import numpy as np                                #import numpy for matrices, and other general mathematical functions
import infrastructures_results                    #import self-made module infrastructures_results for all interactive plotting
import infrastructures_gui                        #import self-made module infrastructurees_gui to run from GUI by default
import infrastructures_interactive_plotting       #import self-made module infrastructurees_interactive_plotting to run interactive plot
import scipy
import final_pdf
import scipy.optimize as optimize
from fpdf import FPDF
from scipy.optimize import LinearConstraint
import pandas as pd
import json

leg = ""

def infrastructures(n0, repair_factors, nLoss, tLoss, timeSpan, nRun, paramTypes, paramIndexes,
                    infStoichFactor, printProgress, averaging, confIntervals, seedValue, imageFileName, remediationFactor, contamination,
                    backups, backupPercent, daysBackup, depBackup, orders, coeffs, ks, negatives):

    '''
    This function calls Gillespie_model to simulate the situational
    efficiencies of interconnected infrastuctures during outages that are
    caused by a public disease outbreak. If one simulation of the
    Gillespie model is run, the function plots a time profile of both the
    disease progression and the infrastructure efficiencies. Otherwise,
    3 plots will be displayed: an example disease time profile, an example
    infrastructure time profile, and a histogram of some desired parameter.

    This function takes up to 15 parameters, but has default values for all:

        n0: an integer tuple of length 16 that stores the initial values of
        efficiencies at the onset of an infrastructure outage of the following
        infrastructures: water (W), energy (E), transport services (T),
        communications services (C), government facilities (G), information
        technology (I), healthcare (H), food and agriculture (A), emergency
        services (S), financial/banking (B), chemical (X), commercial
        facilities (F), manufacturing (M), dams (D), defense (Y), and 
        nuclear (N). Default is (100,50,100,100,100,100,100,100,100,100,100,
        100,100,100,100,100)

        p0: an integer tuple of length 4 that stores initial values of healthy
        people, sick people, immunized people, and dead people respectively in
        response to a public health emergency that causes the infrastructure
        outages. Default is (699900, 100, 0, 0)

        repair_factors: a float tuple of length 16 that stores values for the 
        coefficients of the stoichiometric repair factors. Indices are in the
        same order as the infrastructures in n0. Default is
        (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0)

        nLoss: the additional reduction of efficiency (%) that occurs for each 
        infrastructure at time tLoss. Default is (0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        tLoss: the time (in days) at which an additional infrastructure outage
        occurs. Default is None

        timeSpan: the maximum time (in days) that the simulations can run for.
        Default is 240 days

        nRun: the number of stochastic simulations being run. If 1, a time 
        profile of the disease outbreak and the infractructure efficiencies is 
        plotted. Otherwise, both the time profiles and a histogram of the 
        specified parameters in paramIndexes and paramtypes for each run is 
        plotted. Default is 1

        paramTypes: a string variable that determines the type of the parameter
        that is plotted in each histogram. Supported parameters include the
        minimum value (enter "min"), maximum value (enter "max"), final value
        over the timespan of the simulation (enter "final_val"), time required
        to return to 100% sector efficiency (enter "recover_time"), and average
        (enter "average"). Default is ["min"]

        paramIndexes: the indexes of the infrastructure of which the histogram
        analyses are being carried out. Indexes are the same as n0. Default
        is [0] (water)

        infStoichFactor: a constant that is multiplied to each stoichiometric
        equation in the infrastructure reactions in order to emphasize
        or de-emphasize the effects of interconnected infrastructure in
        relation to the effects of the disease outbreak itself. Default is
        0.01

        printProgress: a boolean switch that determines whether or not the
        current progress is displayed. If more than one run, displays the
        current run. If only one run, displays the current day. Default is
        False

        averaging: a boolean switch that determines whether or not the
        results from each run are averaged together or if an example
        plot is generated instead to improve performance. Default is True

        confIntervals: a boolean switch that determines whether or not the
        confidence interval range is plotted or not. Default is True

        agent: a string variable that ultimately sets the mortality rates of 
        the disease outbreak portion, which determines the ratio of recovery
        to death and therefore kv1 and kv2. Supported agents are anthrax, 
        ebola, and monkeypox for now. Default is anthrax

    This function returns nothing, but it can be made to return something if
    you want it to...
    '''
    #Calculations

    #seed random number generator if desired
    if seedValue is not None:
        np.random.seed(seedValue)
    sensitivity = []
    reportname = "report_inputs.txt"
    data = open(reportname)
    json_data = json.load(data)
    for sector in json_data:
        if(json_data[sector]["sensitivity"]>0):
            sensitivity.append(json_data[sector]["index"])
        if(json_data[sector]["graph"]):
            paramIndexes.append(json_data[sector]["index"])
            paramTypes.append("recovery_time")     
    #initialize param_vals if more than one stochastic simulation is running
    if nRun > 1:
        param_vals = np.zeros((len(paramTypes), nRun), dtype = float)
    else:
        param_vals = None

    if averaging and nRun > 1:
        bin_size = 1
        averages = np.zeros((int(timeSpan/bin_size), 9), dtype = float)
        num_in_bin = np.zeros(int(timeSpan/bin_size), dtype = int)
    else:
        averages = None
        bin_size = None
    #call Gillespie_model nRun times to fetch t and n data for the stochastic solution
    time_of_recovery_vals = np.zeros((len(n0), nRun), dtype = float)
    
    for i in range (0, nRun):
        if printProgress and nRun > 1:
            print("Run " + str(i))
            t, n, contam = Gillespie_model(n0, repair_factors, nLoss, tLoss, timeSpan,
                                              infStoichFactor, False, contamination, remediationFactor, backups, 
                                              backupPercent, daysBackup, depBackup, orders, coeffs, ks, negatives, imageFileName)
        elif printProgress:
            t, n, contam = Gillespie_model(n0, repair_factors, nLoss, tLoss, timeSpan, agent, 
                                              infStoichFactor, True, contamination, remediationFactor, backups, 
                                              backupPercent, daysBackup, depBackup, orders, coeffs, ks, negatives, imageFileName)
        else:
            t, n, contam = Gillespie_model(n0, repair_factors, nLoss, tLoss, timeSpan,
                                              infStoichFactor, False, contamination, remediationFactor, backups, 
                                              backupPercent, daysBackup, depBackup, orders, coeffs, ks, negatives, imageFileName)
        if averaging and nRun > 1:
            for j in range(0, int(timeSpan/bin_size)):
                for k in range(0, len(n)):
                    if t[k] >= j*bin_size and t[k] < j*bin_size+bin_size:
                        averages[j] += n[k]
                        num_in_bin[j] += 1
                    elif t[k] > j*bin_size+bin_size:
                        break
        fileLoc = "report_inputs.txt"
        json_data = open(fileLoc)


        #if making a histogram, retrieve the desired parameter of each solution and store in param_vals if more than 1 stochastic solution is running
        sectorRange = list(range(len(n0)))
        if nRun > 1:
            for m in range(len(sectorRange)):
                if min(n[:,sectorRange[m]]) >= 100:
                    continue #leave a zero in the array whenever the sector efficiency never falls below 100%
                else:
                    time_of_recover = 0
                    time_of_min = np.argmin(n[:,sectorRange[m]])
                    for k in range(time_of_min, len(n[:,sectorRange[m]])):
                        if n[k][sectorRange[m]] > 100:
                            time_of_recover = k
                            break
                    if time_of_recover == 0:
                        time_of_recovery_vals[m][i] = timeSpan
                    else:
                        time_of_recovery_vals[m][i] = t[time_of_recover]
            for j in range(len(paramTypes)):
                if paramTypes[j] == "min":
                    param_vals[j][i] = min(n[:,paramIndexes[j]])
                elif paramTypes[j] == "max":
                    param_vals[j][i] = max(n[:,paramIndexes[j]])
                elif paramTypes[j] == "average":
                    param_vals[j][i] = statistics.mean(n[:,paramIndexes[j]])
                elif paramTypes[j] == "final_val":
                    param_vals[j][i] = n[-1,paramIndexes[j]]
                else: #recover_time
                    if min(n[:,paramIndexes[j]]) >= 100:
                        continue #leave a zero in the array whenever the sector efficiency never falls below 100%
                    else:
                        #find the first index where the efficiency sector hits 100% efficiency after the minimum value occurs
                        time_of_recover = 0
                        time_of_min = np.argmin(n[:,paramIndexes[j]])
                        for k in range(time_of_min, len(n[:,paramIndexes[j]])):
                            if n[k][paramIndexes[j]] > 100:
                                time_of_recover = k
                                break
                        if time_of_recover == 0:
                            param_vals[j][i] = timeSpan
                        else:
                            param_vals[j][i] = t[time_of_recover]


    #divide running sums stored in averages and make into run-averages
    if averaging and nRun > 1:
        for i in range(0, int(timeSpan/bin_size)):
            if num_in_bin[i] == 0:
                if i == 0:
                    averages[i] = n0
                else:
                    averages[i] = averages[i-1]
            else:
                for j in range(0,len(averages[i])):
                    averages[i][j] = averages[i][j]/num_in_bin[i]

    #Plotting
    infrastructures_results.results(nRun, paramTypes, paramIndexes, param_vals, imageFileName, contam, int(timeSpan))
    #make interactive plot of infrastructure efficiency time profiles
    if averages is not None:
        bin_t = np.arange(0, timeSpan, bin_size)
##        fig, ax, leg = infrastructures_interactive_plotting.plotting(bin_t,averages,timeSpan)
        fig, ax, leg = infrastructures_interactive_plotting.plotting(t,n,None, None, timeSpan, imageFileName, contam)
    else:
        fig, ax, leg = infrastructures_interactive_plotting.plotting(t,n,None, None, timeSpan, imageFileName, contam)
    #fig, ax, leg = infrastructures_interactive_plotting.plotting(t,n,timeSpan)

    
    #ranking the priorities by coefficients
    ranked_dict, ranked = prioritizeByConnections(orders, list(range(len(n0))))
    ranked_dict_rt, ranked_rt = getRecoveryTimeDict(time_of_recovery_vals, sectorRange)
    f = open("Results/" + imageFileName + "_prioritization.txt", "w")
    f.write("Rank by strength of connections: \n")
    i = 1
    sectors = []
    for key, value in ranked_dict:
        f.write(str(i) + ")" + str(key) + " : " + str(round(float(value), 2))+ "\n")
        i += 1
    f.write("\nRank by median recovery time: \n")
    i = 1
    results = pd.DataFrame()
    sectors = []
    recoveryTimes = []
    for key, value in ranked_dict_rt:
        f.write(str(i) + ")" + str(key) + " : " + str(round(float(value), 2))+ " days \n")
        i += 1
        sectors.append(key)
        recoveryTimes.append(str(round(float(value), 2)))
    #final_pdf.createPdf(ranked_dict, ranked_dict_rt, imageFileName, sensitivity, paramIndexes, paramTypes)
    results["Sectors"] = sectors
    results["Recovery Times"] = recoveryTimes
    results.to_csv("Results/" + imageFileName + ".csv")
    f.close()
    

    #end program without returning anything
    return leg

def getRecoveryTime(remediationFactor, n0, repair_factors, nLoss, tLoss, timeSpan, infStoichFactor, printProgress, contamination):
    t, n, contam = Gillespie_model(n0, repair_factors, nLoss, tLoss, timeSpan, infStoichFactor, False, contamination, remediationFactor)
    recoveryTimes = []
    for i in range(len(contamination)):
        time_of_min = np.argmin(n[:,i])
        time_of_recover = 100
        if min(n[:,i]) >= 100:
            time_of_recover = 0
        else:
            for k in range(time_of_min, len(n[:,i])):
                if n[k][i] > 100:
                    time_of_recover = k
                    break
        recoveryTimes.append(time_of_recover)
    print(sum(remediationFactor))
    return sum(recoveryTimes)

def constraintsFunction(x0, maxPercent):
    return sum(x0) - maxPercent

def optimizeDecon(n0, p0, repair_factors, nLoss, tLoss, timeSpan, nRun, paramTypes, paramIndexes,
                    infStoichFactor, printProgress, averaging, confIntervals, agent, seedValue, imageFileName, remediationFactor,
                  contamination, maxPercent):
    x0 = [0]*len(remediationFactor)
    for i in range(len(remediationFactor)):
        x0[i] = float(remediationFactor[i])
    args = (n0, p0, repair_factors, nLoss, tLoss, timeSpan, agent, infStoichFactor, False, contamination)
    my_constraints = ({'type': 'ineq', 'fun': lambda x: np.array([maxPercent - sum(x)])})
    linear_constraint = LinearConstraint([[1,0,0,0,0,0,0,0,0], 
    [0,1,0,0,0,0,0,0,0], 
    [0,0,1,0,0,0,0,0,0], 
    [0,0,0,1,0,0,0,0,0], 
    [0,0,0,0,1,0,0,0,0], 
    [0,0,0,0,0,1,0,0,0], 
    [0,0,0,0,0,0,1,0,0], 
    [0,0,0,0,0,0,0,1,0], 
    [0,0,0,0,0,0,0,0,1], 
    [1,1,1,1,1,1,1,1,1]], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [float(maxPercent), float(maxPercent), float(maxPercent), float(maxPercent), float(maxPercent), float(maxPercent), float(maxPercent), float(maxPercent), float(maxPercent), float(maxPercent)])
    maxPercent = float(maxPercent)
    bnds = ((0,float(maxPercent)), (0, float(maxPercent)), (0, float(maxPercent)), (0, float(maxPercent)), (0, float(maxPercent)), (0, float(maxPercent)), (0, float(maxPercent)), (0, float(maxPercent)), (0, float(maxPercent)))
    result = scipy.optimize.minimize(getRecoveryTime, x0, args, constraints = my_constraints,bounds =bnds)
    return result

def adjustContamination(contamination, remediationFactor, timestep):
    results = [0] * len(contamination)
    for c in range(len(contamination)):
        cpercent = float(contamination[c])
        r = float(remediationFactor[c])
        if contamination[c] < 100 :
            results[c] = cpercent + r*timestep
        else:
            results[c] = 100
    return results

def get_sector_name(sector):
    if sector == 0:
        return "Water and Wastewater Systems"
    elif sector == 1:
        return "Energy"
    elif sector == 2:
        return "Transportation Systems"
    elif sector == 3:
        return "Communications"
    elif sector == 4:
        return "Government Facilities"
    elif sector == 5:
        return "Food and Agriculture"
    elif sector == 6:
        return "Emergency Services"
    elif sector == 7:
        return "Waste Management"
    elif sector == 8:
        return "Healthcare"

def prioritizeByConnections(orders, sectors):
    orders = np.transpose(orders)
    results = {}
    for i in range(len(sectors)):
        name = get_sector_name(sectors[i])
        results[name] = sum(orders[i])
    results_final = sorted(results.items(), key=lambda x: x[1], reverse=True)
    ranked = []
    for key in results_final:
        ranked.append(key)
    return results_final, ranked

def getRecoveryTimeDict(recoveryTimes, sectors):
    results = {}
    ranked = []
    for i in range(len(recoveryTimes)):
        name = get_sector_name(sectors[i])
        recovery_time = np.percentile(recoveryTimes[i],50)
        results[name] = recovery_time
    results_final = sorted(results.items(), key=lambda x: x[1], reverse=True)
    for key in results_final:
        ranked.append(key)
    return results_final, ranked

def Gillespie_model(n0, repair_factors, nLoss, tLoss, timeSpan, infStoichFactor, printProgress, contamination,
                    remediationFactor, backups, backupPercents, daysBackup, depBackup, orders0, coeffs0, ks0,
                    negatives, imageFileName):
    '''
    This function simulates interconnected infrastructures using the Gillespie
    algorithm to stochastically determine the efficiencies of the water,
    energy, transport, communications, government, and IT infrastructures in
    the event of an outage.

    This function takes 12 of the 15 parameters from infrastructures() with the
    exception of nRun, paramType, and paramIndex

    This function returns an array t_vals (which stores the values of t at each
    timestep) and n (which stores the efficiency values at each timestep).
    '''

    #initialize the kv (virus rate constants) dependent on agent
##    if agent == "monkeypox":
##        R0 = 1.2                    #source: Smith 2013
##        time_to_recovery = 20.5     #source: Jezek et al 1988
##        mortality_rate = 0.098      #source: Hutin et al 2001 (treated!)
##    elif agent == "anthrax":
##        R0 = 0.0                    #anthrax is not infectious
##        time_to_recovery = 22.1     #source: Holty et al 2006
##        mortality_rate = 0.5        #source: FDA 2018 (treated!)
##    elif agent == "ebola":
##        R0 = 1.85                   #source: Althaus 2014
##        time_to_recovery = 17.5     #source: Francesconi et al 2003
##        mortality_rate = 0.5        #source: WHO 2017 (treated!)
##    elif agent == "natural_disaster":
    R0 = 0.0                   #source: Althaus 2014
    time_to_recovery = 0.0     #source: Francesconi et al 2003
    mortality_rate = 0.0        #source: WHO 2017 (treated!)

    kv0 = R0*0.00000003
    kv12sum = time_to_recovery * 0.001
    kv1 = kv12sum * (1.0-mortality_rate)
    kv2 = kv12sum * mortality_rate

    #define the rate constants for the infrastructure reactions (equal and unequal exponent versions)
    '''
    k = np.array([2.15443469003188, 4.64158883361278, 0.215443469003188, 3.16227766, \
                  0.000879923, 14.6779926762207, 1.46779926762207, 21.5443469003188, \
                  6.81292069057961E-06, 0.316227766, 10.00000000, 0.000146780, \
                  4.641588834, 68.12920690, 1.000000000, 4.641588834])


    k = np.array([1e-8, 1e-8, 1e-6, 1e-6, \
                  1e-12, 1e-6, 1e-6, 1e-4, \
                  1e-10])






    k = np.array([0.040046457, 0.1701254, 0.00702, 0.083767764, \
                  0.002154435, 4.12463, 0.49239, 24.2446201708233, \
                  2.8942E-06])


    #define the reaction orders for the infrastructure reactions (equal and unequal exponent versions)




    #PATH/AWARE Single Decon Single
    k = np.array([0.00139, 0.00518, 0.00518, 0.01, \
                  0.268, 0.5179, 0.5179, 7.197, \
                  0.0373])

    #PATH/AWARE Single Decon large exponent
    k = np.array([3.81024E-05, 0.000185, 0.000185, 0.000485, \
                  0.0604, 0.1585, 0.1166, 5.532, \
                  0.00334])

    #PATH/AWARE Single
    k = np.array([0.00268, 0.01, 0.01, 0.01931, \
                  0.5179, 1, 1, 13.894, \
                  0.07197])

    orders = np.array([[0.250, 0.417, 0.083, 0.000, 0.000, 0.000, 0.000, 0.083, 0.000], \
                       [0.000, 0.333, 0.083, 0.167, 0.083, 0.000, 0.000, 0.000, 0.000], \
                       [0.000, 0.500, 0.750, 0.083, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.000, 0.417, 0.000, 0.333, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.750, 0.500, 0.167, 0.556, 0.111, 0.222, 0.000, 0.000, 0.000], \
                       [0.000, 0.000, 0.167, 0.000, 0.167, 0.083, 0.167, 0.000, 0.444], \
                       [0.000, 0.167, 0.167, 0.583, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.083, 0.083, 0.167, 0.000, 0.000, 0.000, 0.000, 0.083, 0.000], \
                       [0.917, 0.667, 1.000, 0.083, 0.000, 0.000, 0.000, 0.000, 0.917]]
                      )
    '''
    #contOrder = np.array([0.583, 0.333, 0.583, 0.417, 2.0, 0.333, 0.917, 0.333, 2.667])
    
    #contOrder = np.array([1.462, 1.077, 1.385, 1.231, 2.231, 0.615, 1.154, 0.333, 2.667])

    
    orders = orders0
    ks = ks0
    '''
    orders = np.array([[0.333, 0.417, 0.250, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.333, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.000, 0.333, 0.083, 0.167, 0.083, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.083, 0.000, 0.083], \
                       [0.000, 0.500, 0.750, 0.083, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.000, 0.417, 0.000, 0.333, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.750, 0.500, 0.167, 0.417, 0.083, 0.000, 0.333, 0.167, 0.000, 0.000, 0.000, 0.167, 0.000, 0.000, 0.083, 0.000], \
                       [0.000, 0.083, 0.000, 0.167, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.917, 0.667, 1.000, 0.000, 0.083, 0.000, 0.917, 0.000, 0.167, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.000, 0.000, 0.167, 0.000, 0.167, 0.000, 0.000, 0.083, 0.000, 0.000, 0.000, 0.083, 0.000, 0.000, 0.000, 0.000], \
                       [0.000, 0.167, 0.167, 0.583, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.000, 0.000, 0.083, 0.750, 0.000, 0.250, 0.000, 0.000, 0.000, 0.167, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.000, 0.000, 0.250, 0.000, 0.083, 0.000, 0.000, 0.000, 0.000, 0.000, 0.167, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.583, 0.417, 0.250, 0.250, 0.583, 0.000, 0.167, 0.083, 0.333, 0.167, 0.000, 0.083, 0.000, 0.000, 0.000, 0.000], \
                       [0.083, 0.083, 0.333, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.167, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.083, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000], \
                       [0.167, 0.167, 0.417, 0.000, 0.000, 0.000, 0.083, 0.000, 0.083, 0.000, 0.000, 0.083, 0.000, 0.000, 0.000, 0.000], \
                       [0.000, 0.000, 0.167, 0.083, 0.000, 0.083, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.333]])

    #PATH/AWARE Single

    orders = np.array([[0.143, 0.857, 0.429, 0.286, 0, 0.143, 0.143, 0.143, 0.143], \
                       [0.714, 0.143, 0.429, 0.571, 0.143, 0, 0, 0, 0], \
                       [0.571, 1, 0.143, 0.286, 0, 0, 0, 0, 0], \
                       [0.429, 1, 0.286, 0.143, 0, 0, 0, 0, 0], \
                       [0.286, 0.143, 0.143, 0.143, 0.143, 0.143, 0, 0, 0.143], \
                       [0.143, 0.286, 0.286, 0, 0.143, 0.143, 0, 0, 0], \
                       [0.286, 0.286, 0.143, 0.286, 0, 0, 0, 0, 0], \
                       [0.143, 0.143, 0.143, 0, 0, 0, 0, 0, 0], \
                       [0.429, 0.429, 0.286, 0.143, 0.143, 0, 0, 0, 0.143]])


 
    orders = np.array([[1, 1, 1, 1, 0, 1, 1, 1, 1], \
                       [1, 1, 1, 1, 1, 0, 0, 0, 0], \
                       [1, 1, 1, 1, 0, 0, 0, 0, 0], \
                       [1, 1, 1, 1, 1, 0, 0, 0, 0], \
                       [1, 1, 1, 1, 1, 1, 0, 0, 1], \
                       [0, 1, 1, 0, 1, 1, 0, 0, 0], \
                       [1, 1, 1, 1, 0, 0, 0, 0, 0], \
                       [1, 1, 1, 0, 0, 0, 0, 0, 0], \
                       [1, 1, 1, 1, 1, 1, 0, 0, 1]])

    
    orders = np.array([[0.231, 0.769, 0.231, 0.154, 0, 0.077, 0.077, 0.077, 0.077], \
                       [0.385, 0.308, 0.231, 0.385, 0.077, 0, 0, 0, 0], \
                       [0.308, 0.923, 0.692, 0.154, 0, 0, 0, 0, 0], \
                       [0.231, 0.846, 0.154, 0.308, 0.0, 0, 0, 0, 0], \
                       [0.769, 0.462, 0.154, 0.385, 0.077, 0.154, 0, 0, 0.308], \
                       [0.077, 0.154, 0.231, 0, 0.154, 0.077, 0, 0, 0], \
                       [0.154, 0.231, 0.154, 0.615, 0, 0, 0, 0, 0], \
                       [0.077, 0.077, 0.154, 0, 0, 0, 0, 0, 0], \
                       [1.000, 0.769, 1.00, 0.077, 0.077, 0, 0, 0, 0.846]])
                       
   '''
    #single
    #contOrder = np.array([0.143, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143])
    #contOrder = np.array([1.00, 0.846, 1.308, 1.231, 1.923, 0.462, 1.077, 0.308, 2.846])
    #contOrder = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00])
    contOrder = np.array([1.0, 0.867, 0.867, 0.8, 0.467, 0.4, 0.467, 0.2, 0.667])
    
    #define a bed-efficiency constant that associates hospital beds relating to healthcare infrastructure efficiency. Based on number of hospital beds in Denver. Automatically deduct initial sickesses
    num_beds = 11227                #source: Colorado Hospital Association (CHA) DATABANK Program, 2017
    bed_const = 1.0/num_beds*100

    #preallocate arrays for the t and n values
    nMax = 10000000 #arbitrary maximum limit of reactions, merely used in preallocating a large enough array
    t_vals = np.zeros(nMax)
    n = np.zeros((nMax, 9))
    cResults = np.zeros((nMax, 9))
    p = np.zeros((nMax, 4))

    #set the first line of n to be n0, and p to be p0, setting the initial condition
    n[0,:] = n0
    #p[0,:] = p0

    #declare t, printed_t, and index as the current time, time to display on the console for tracking progress, and number of reactions respectively
    t = 0
    if printProgress:
        printed_t = 0
    index = 1

    #declare a boolean added to determine if the additional infrastructure outage has occured yet. Only applies when tLoss is not equal to None
    added = False

    #loop until the maximum number of reactions are run (or if a break statement is encountered)
    while index < nMax:

        #if at the first timestep automatically deduct the healthcare efficiency by the number of people who get sick by the number of people who initially get infected. If result is negative, set to be infStoichFactor (small)
        if index == 1:
            #n[index-1][8] -= p[index-1][1]*bed_const
            if n[index-1][8] <= 0:
                n[index-1][8] = infStoichFactor

        #calculate the ratio of healthy people to all people (healthy, sick, immune, dead)
        #healthy_ratio = (p[index-1][0]+p[index-1][2])/sum(p0)

        #define a "repair factor" for each infrastructure that defines the rate at which society works harder to put infrastructures back online, adjusted by ratio of healthy people able to work and the infStoichFactor
        adj_repair_factors = 9*[0.0]
        for i in range(0, len(adj_repair_factors)):
            #adj_repair_factors[i] = (repair_factors[i]/infStoichFactor)*healthy_ratio
            adj_repair_factors[i] = (repair_factors[i]/infStoichFactor)
        
        #calculate the rates of each infrastructure 'reaction'
        r = 9*[0.0]
        for i in range (0, len(r)):
            r[i] = ks[i]
        for i in range(0, len(orders)):
            backupI = []
            backupE = []
            backupTime = []
            if depBackup != None:
                for dp in range(0, len(depBackup)):
                    if int(depBackup[dp]) == i:
                        if (backups[dp]) not in backupI: 
                            backupI = np.append(backupI,backups[dp])
                            backupE = np.append(backupE,backupPercents[dp])
                            backupTime = np.append(backupTime, daysBackup[dp])
            for j in range(0, len(orders[i])):
                if j in backupI:
                    time_index = np.where(backupI == j)
                    if t< backupTime[time_index]:
                        r[i] = r[i]*float(backupE[time_index])**orders[i][j]
                    else:
                        
                        r[i] = r[i]*(n[index-1][j])**orders[i][j]
                else:
                    r[i] = r[i]*(n[index-1][j])**orders[i][j]
        for i in range (0, len(r)):
            r[i] = r[i]/n[index-1][i]
        for i in range(0, len(n[index-1])):
            if (n[index-1][i] >= 100):
                r[i] = 0
        #adjust for the contamination
        
        #for c in range(len(contamination)):
            #if (contamination[c] > 0):
                #r[c] = r[c]*(contamination[c])**contOrder[c]

        #calculate the rates of each virus 'reaction'
        #rv0 = kv0*p[index-1][0]*p[index-1][1]
        #rv1 = kv1*p[index-1][1]
        #rv2 = kv2*p[index-1][1]

        rv0 = kv0*p[index-1][0]*p[index-1][1]
        rv1 = kv1*p[index-1][1]
        rv2 = kv2*p[index-1][1]

        #calculate rtotal as the sum of all rates and finish the simulation if rtotal = 0. If stockpiling, do not add rate if an infrastructure is at 100% (no reactions can happen anymore. Pretty sure this can't happen with these reactions)
        rtotal = sum(r) + rv0 + rv1 + rv2
        #generate a random number from 0 to 1 to determine the interval of time at this timestep, as per the Gillespie algorithm
        rand_num = np.random.rand()
            
        if rtotal == 0:
            #truncate the length of the n and t arrays, as nMax reactions were not achieved
            tau = 1
            n = np.delete(n, np.s_[(index):], 0)
            #p = np.delete(p, np.s_[(index):], 0)
            while (t < timeSpan):
                if (all(i >= 100 for i in contamination)):
                    break
                contamination = adjustContamination(contamination, remediationFactor, tau)
                t_vals[index] = t
                cResults[index] = contamination
                t = t+tau
                index += 1

            t_vals = np.delete(t_vals, np.s_[(index):], 0)
            cResults = np.delete(cResults, np.s_[(index):], 0)
            #break from the loop, end simulation
            break
            
        #use the formula given in the Gillespie slides to determine the length of time of the current timestep, increment t by this value
        tau = -np.log(rand_num)/rtotal
        contamination = adjustContamination(contamination, remediationFactor, tau)
        t = t + tau

        if printProgress:
            if t//1 > printed_t:
                printed_t = t//1
                print("Day " + str(int(printed_t)))

        #break from the loop if the maximum timeSpan is reached for the simulation
        if t > timeSpan:

            #truncate the n and t_vals arrays as nMax reactions were not achieved (this is possible unlike the case where no more reacitons can occur)
            n = np.delete(n, np.s_[(index):], 0)
            #p = np.delete(p, np.s_[(index):], 0)
            t_vals = np.delete(t_vals, np.s_[(index):], 0)
            cResults = np.delete(cResults, np.s_[(index):], 0)

            #break from the loop, end simulation
            break

        #store the current t value in the preallocated array
        t_vals[index] = t

        #if the additional infrastructure outage has not occurred yet, check if the current time is past tLoss and then implement the infrastructure outage if this is the case
        if tLoss != None and not added:
            if t > tLoss:
                n[index-1] = n[index-1] - nLoss
                added = True

        #based on the calculated rate and the sum of all rates, calculate the probability that each reaction is going to occur at the current timestep
        probabilities = r/rtotal
        probabilities = np.append(probabilities, rv0/rtotal)
        probabilities = np.append(probabilities, rv1/rtotal)
        probabilities = np.append(probabilities, rv2/rtotal)

        #calculate the csp vector, the sum of probabilities (cumulative probabilities)
        csp = [0]*12
        sum_p = 0
        for i in range(0,12):
            sum_p += probabilities[i]
            csp[i] = sum_p

        #generate another random value from 0 to 1 to be used to determine which reaction occurs based on the cumulative probabilities of each reaction
        q = np.random.rand()

        #declare v, the change in each n or p value at the current timestep based on the 'stoichiometry' of which reaction occurs, determined by q (randomly generated).
        
        # coeffs = [[0.583, -0.417, -0.083, 0.000, 0.000, 0.000, 0.000, -0.083, 0.000], \
                  # [0.000, 0.333, -0.083, -0.167, -0.083, 0.000, 0.000, 0.000, 0.000], \
                  # [0.000, -0.500, 0.583, -0.083, 0.000, 0.000, 0.000, 0.000, 0.000], \
                  # [0.000, -0.417, 0.000, 0.417, 0.000, 0.000, 0.000, 0.000, 0.000], \
                  # [-0.750, -0.500, -0.167, -0.417, 2.000, -0.167, 0.000, 0.000, -0.444], \
                  # [0.000, 0.000, -0.167, 0.000, -0.167, 0.333, 0.000, 0.000, 0.000], \
                  # [0.000, -0.167, -0.167, -0.583, 0.000, 0.000, 0.917, 0.000, 0.000], \
                  # [-0.083, -0.083, -0.167, 0.000, 0.000, 0.000, 0.000, 0.333, 0.000], \
                  # [-0.917, -0.667, -1.000, 0.000, -0.083, 0.000, 0.000, 0.000, 2.667]]
        '''
        coeffs = [[4.0, -1.0, -1.0, -1.000, 0.000, 0.000, 0.000, -1.0, 0.000], \
          [-1.0, 4.0, -1.0, -1.0, -1.000, 0.000, 0.000, 0.000, 0.000], \
          [-1.0,-1.0, 3.0, -1.0, 0.000, 0.000, 0.000, 0.000, 0.000], \
          [-1.0, -1.0, -1.0, 3.0, 0.000, 0.000, 0.000, 0.000, 0.000], \
          [-1.0, -1.00, -1.00, -1.00, 6.000, -1.0, 0.000, 0.000, -1.0], \
          [0.000, -1.0, -1.0, 0.000, -1.00, 3.0, 0.000, 0.000, 0.000], \
          [-1.0, -1.0, -1.00, -1.000, 0.000, 0.000, 4.0, 0.000, 0.000], \
          [-1.0, -1.0, -1.00, 0.000, 0.000, 0.000, 0.000, 3.0, 0.000], \
          [-1.0, -1.0, -1.0, -1.0, -1.0, 0.000, 0.000, 0.000, 5.0]]
        


        coeffs = [[2.143, -0.857, -0.429, -0.286, 0.000, -0.143, -0.143, -0.143, -0.143], \
          [-0.714, 1.571, -0.143, -0.571, -0.143, 0.000, 0.000, 0.000, 0.000], \
          [-0.571,-1.000, 1.875, -0.286, 0.000, 0.000, 0.000, 0.000, 0.000], \
          [-0.429, -1.0, -0.286, 1.714, 0.000, 0.000, 0.000, 0.000, 0.000], \
          [-0.286, -0.143, -0.143, -0.143, 1.000, -0.143, 0.000, 0.000, -0.143], \
          [-0.143, -0.286, -0.286, 0.000, -0.143, 0.857, 0.000, 0.000, 0.000], \
          [-0.286, -0.286, -0.143, -0.286, 0.000, 0.000, 1.0, 0.000, 0.000], \
          [-0.143, -0.143, -0.143, 0.000, 0.000, 0.000, 0.000, 0.429, 0.000], \
          [-0.429, -0.429, -0.286, -0.143, -0.143, 0.000, 0.000, 0.000, 1.429]]

        #PATH/AWARE Single
        coeffs = [[1.462, -0.769, -0.231, -0.154, 0.000, -0.077, -0.077, -0.077, -0.077], \
          [-0.385, 1.077, -0.231, -0.385, -0.077, 0.000, 0.000, 0.000, 0.000], \
          [-0.308,-0.923, 1.385, -0.154, 0.000, 0.000, 0.000, 0.000, 0.000], \
          [-0.231, -0.846, -0.154, 1.231, 0.000, 0.000, 0.000, 0.000, 0.000], \
          [-0.769, -0.462, -0.154, -0.385, 2.231, -0.154, 0.000, 0.000, -0.308], \
          [-0.077, -0.154, -0.154, 0.000, -0.154, 0.615, 0.000, 0.000, 0.000], \
          [-0.154, -0.231, -0.154, -0.615, 0.000, 0.000, 1.154, 0.000, 0.000], \
          [-0.077, -0.077, -0.154, 0.000, 0.000, 0.000, 0.000, 0.308, 0.000], \
          [-1.00, -0.769, -1.0, -0.077, -0.077, 0.000, 0.000, 0.000, 2.923]]
'''
        #print(coeffs[0][0], coeffs0[0][0])

        
        coeffs = coeffs0.copy()

        v = []

        reaction = 0
        while q > csp[reaction]:
            reaction += 1

        #when len(v) is 9, an infrastructure equation is being applied
        if reaction <= 9:
            backupI = []
            backupDays = []
            if depBackup != None:
                for dp in range(0, len(depBackup)):
                    if int(depBackup[dp]) == reaction:
                        backupI = np.append(backupI,backups[dp])
                        backupDays = np.append(backupDays, daysBackup[dp])
            v = coeffs[reaction]
            v[reaction] += adj_repair_factors[reaction]
            for b in range(0, len(backupI)):
                if t<backupDays[b]:
                    v[int(backupI[b])] = 0
            if not negatives:
                for b in range(0, len(coeffs[reaction])):
                    if b != reaction:
                        v[b] = 0

        #otherwise a disease outbreak equation is being applied. Done 10 at a time to reduce computational time
        elif q < csp[8]:
            v = [-10, 10, 0, 0]
        elif q < csp[11]:
            v = [0, -10, 10, 0]
        else:
            v = [0, -10, 0, 10]

        #set the n or p values based on v and the n or p values at the previous timestep, multiply v vector by infStoichFactor if applicable
        if len(v) == 9:
            v = [x * infStoichFactor for x in v]
            cResults[index] = contamination
            test = n[index-1] + v
            
            for i in range(len(test)):
                if test[i] > contamination[i] and contamination[i] < 100:
                    n[index][i] = contamination[i]
                else:
                    n[index][i] = test[i]
            #p[index] = p[index-1]
            
        else:
            #p[index] = p[index-1] + v
            n[index] = n[index-1]
            #increment or decrement healthcare infrastructure by bed_const depending on if person got sick or left hospital (either due to death or recovery)
            if q > csp[8] and p[index][1] < num_beds:
                n[index][6] += bed_const
            else:
                n[index][6] -= bed_const
        #if, for some reason one of the infrastructure efficiency values falls below 0 (easier to do with floats than int), reset the value to be the infStoichFactor. Set up consts to not reach this point!
        for infrastructure in range(len(n[index])):
            if n[index][infrastructure] <= 0:
                n[index][infrastructure] = infStoichFactor
            if n[index][infrastructure] >= 110:
                n[index][infrastructure] = 110

        #increment the number of reactions
        index += 1

    #return the t and n data to be plotted
    return t_vals,n,cResults

if __name__ == '__main__':
    infrastructures_gui.main()
