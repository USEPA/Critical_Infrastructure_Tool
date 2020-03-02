# -*- coding: utf-8 -*-
"""
infrastructures_from_file.py
Created on Wed Jun 19 15:12:06 2019
Created by: Mitchell Wendt
Revised: 08/28/2019
Revised by: Mitchell Wendt
"""

import numpy as np
import warnings
import infrastructures_v4

def run_file(optimize, orders, coeffs, ks):

    #defaults
    n0 = (100,50,100,100,100,100,100,100, 100)
    p0 = (699900, 100, 0, 0)
    repair_factors = None
    nLoss = None
    tLoss = None
    timeSpan = 240.0
    nRun = 1
    paramTypes = None
    paramIndexes = None
    printProgress = False
    averaging = True
    intervals = True
    # agent = 'anthrax'
    seedValue = None
    name = 'results'
    remediationFactor = (1,1,1,1,1,1,1,1,1)
    contamination = (0,0,0,0,0,0,0,0,0)
    maxPercent = 40

    #read file
    fname = "infrastructures_inputs.txt"
    with open(fname) as f:
        contents = f.readlines()

    #loop through input commands in the file, doing parsing and error handling at each command
    for i in range(0, len(contents)):

        values = (contents[i]).split()

        if len(values) < 2:
            warnings.warn("Skipped line " +str(i)+ ", a default value may be entered")
            continue

        if values[0] == "n0":
            values.pop(0)
            if len(values) != 9:
                raise TypeError("exactly 9 values must be entered for n0")
            n_values = np.zeros(9,dtype=float)
            for i in range(0, len(values)):
                try:
                    n_values[i] = float(values[i])
                except:
                    raise ValueError("Inputs to n0 must be float/decimal values")
                if float(values[i]) <= 0 or float(values[i]) > 100:
                    raise ValueError("n0 values must be greater than zero and less than or equal to 100")
            n0 = n_values

        elif values[0] == "p0":
            values.pop(0)
            if len(values) != 4:
                raise TypeError("exactly 4 values must be entered for p0")
            p_values = np.zeros(4,dtype=int)
            for i in range(0, len(values)):
                try:
                    p_values[i] = int(values[i])
                except:
                    raise ValueError("Inputs to p0 must be integers")
                if int(values[i]) < 0:
                    raise ValueError("p0 values must be greater than or equal to zero")
                p0 = p_values

        elif values[0] == "repair_factors":
            values.pop(0)
            if values[0] == "None" or values[0] == "none":
                repair_factors = None
            elif len(values) != 9:
                raise TypeError("exactly 8 values must be entered for repair_factors, or None")
            else:
                rf_values = np.zeros(9,dtype=float)
                for i in range(0, len(values)):
                    try:
                        rf_values[i] = float(values[i])
                    except:
                        raise ValueError("Inputs to repair_factors must be float/decimal values")
                    if float(values[i]) < 0:
                        raise ValueError("repair_factor values must be greater than or equal to zero")
                repair_factors = rf_values

        elif values[0] == "nLoss":
            values.pop(0)
            if values[0] == "None" or values[0] == "none":
                nLoss = None
                tLoss = None
            elif len(values) != 9:
                raise TypeError("exactly 8 values must be entered for nLoss, or None")
            else:
                nloss_values = np.zeros(9,dtype=float)
                for i in range(0, len(values)):
                    try:
                        nloss_values = float(values[i])
                    except:
                        raise ValueError("Inputs to nLoss must be float/decimal values")
                    if float(values[i]) < 0 or float(values[i]) >= 100:
                        raise ValueError("nLoss values must be greater than or equal to zero and less than 100")
                nLoss = nloss_values
            if nLoss is None or nLoss == (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0):
                tLoss = None

        elif values[0] == "tLoss":
            if values[1] == "none" or values[1] == "None" or values[1] == "0":
                tLoss = None
                nLoss = None
            else:
                try:
                    tLoss = float(values[1])
                except:
                    raise TypeError("tLoss must be a float/decimal")
                if tLoss <= 0:
                    raise ValueError("tLoss must be greater than zero")

        elif values[0] == "timeSpan":
            try:
                timeSpan = float(values[1])
            except:
                raise TypeError("Input to timeSpan must be a float/decimal")
            if timeSpan <= 0:
                raise ValueError("timeSpan must be a float/decimal greater than 0")

        elif values[0] == "nRun":
            try:
                nRun = int(values[1])
            except:
                raise TypeError("Input to nRun must be an integer")
            if nRun < 1:
                raise ValueError("nRun must be an integer 1 or greater")

        elif values[0] == "paramTypes":
            values.pop(0)
            if values[0] == "None" or values[0] == "none":
                paramTypes = None
                paramIndexes = None
            else:
                print("list")
                params = []
                
                for i in range(0, len(values)):
                    if values[i] != "min" and values[i] != "max" and values[i] != "average" and values[i] != "final_val" and values[i] != "recover_time":
                        raise ValueError("Unknown parameter type, acceptable values are 'min', 'max', 'average', 'recover_time', and 'final_val'")
                    else:
                        params.append(values[i])
                paramTypes = np.asarray(params)

        elif values[0] == "paramIndexes":
            values.pop(0)
            if values[0] == "None" or values[0] == "none":
                paramTypes = None
                paramIndexes = None
            else:
                params = []
                for i in range(0, len(values)):
                    try:
                        params.append(int(values[i]))
                    except:
                        raise ValueError("Inputs to paramIndexes must be integers")
                    if int(values[i]) < 0 or int(values[i]) > 10:
                        raise ValueError("paramIndexes may only be between 0 and 7")
                paramIndexes = np.asarray(params)

        elif values[0] == "infStoichFactor":
            if values[1] == "None" or values[1] == "none":
                infStoichFactor = None
            else:
                try:
                    infStoichFactor = float(values[1])
                except:
                    raise TypeError("infStoichFactor must be a float/decimal value")
                if infStoichFactor <= 0:
                    raise ValueError("infStoichFactor must be greater than zero")

        elif values[0] == "printProgress":
            if values[1] == "true" or values[1] == "True" or values[1] == "1":
                printProgress = True
            else:
                printProgress = False

        elif values[0] == "averaging":
            if values[1] == "true" or values[1] == "True" or values[1] == "1":
                averaging = True
            else:
                averaging = False

        elif values[0] == "intervals":
            if values[1] == "true" or values[1] == "True" or values[1] == "1":
                intervals = True
            else:
                intervals = False

        elif values[0] == "agent":
            if values[1] != "anthrax" and values[1] != "ebola" and values[1] != "monkeypox" and values[1] != "natural_disaster":
                raise ValueError("Uvaluesupported Agent Name")
            else:
                agent = values[1]

        elif values[0] == "seedValue":
            if values[1] == "none" or values[1] == "None" or values[1] == "false" or values[1] == "False":
                seedValue = None
            else:
                try:
                    seedValue = int(values[1])
                except:
                    raise TypeError("seedValue input must be an integer or 'None'")
        elif values[0] == "name":
            name = values[1]
            
        elif values[0] == "remediationFactor":
            values.pop(0)
            if len(values) != 9:
                raise TypeError("exactly 9 values must be entered for remediationFactors")
            r_values = np.zeros(9,dtype=float)
            for i in range(0, len(values)):
                try:
                    r_values[i] = float(values[i])
                except:
                    raise ValueError("Inputs to n0 must be float/decimal values")
                if float(values[i]) <= 0 or float(values[i]) > 100:
                    raise ValueError("n0 values must be greater than zero and less than or equal to 100")
            remediationFactor = r_values

        elif values[0] == "contamination":
            values.pop(0)
            if len(values) != 9:
                raise TypeError("exactly 9 values must be entered for contamination")
            c_values = np.zeros(9,dtype=float)
            for i in range(0, len(values)):
                try:
                    c_values[i] = 100-float(values[i])
                except:
                    raise ValueError("Inputs to n0 must be float/decimal values")
                if float(values[i]) < 0 or float(values[i]) > 100:
                    raise ValueError("contamination values must be greater than zero and less than or equal to 100")
            contamination = c_values

        elif values[0] == "maxPercent":
            if values[1] == "none" or values[1] == "None" or values[1] == "false" or values[1] == "False":
                maxPercent = None
            else:
                try:
                    maxPercent = float(values[1])
                except:
                    raise TypeError("maxPercent input must be an integer or 'None'")
                if sum(remediationFactor) > maxPercent:
                    raise TypeError("Sum of remediation factors must be less than max percent")

        elif values[0] == "backups":
            values.pop(0)
            if values[0] == "None" or values[0] == "none":
                backup_values = None
            else:
                backup_values = []
                for i in range(0, len(values)):
                    try:
                        backup_values.append(int(values[i]))
                    except:
                        raise ValueError("Inputs to backups must be parameter indexes")
                    if int(values[i]) < 0 or int(values[i]) > 10:
                        raise ValueError("backup values must be greater than zero and less than 10")
            backups = backup_values

        elif values[0] == "backupPercent":
            values.pop(0)
            if values[0] == "None" or values[0] == "none":
                backupPercent_values = None
            elif len(values) != len(backups):
                raise ValueError("backup percents and backup efficiencies must be the same size")
            else:
                backupPercent_values = [] 
                for i in range(0, len(values)):
                    try:
                        backupPercent_values.append(float(values[i]))
                    except:
                        raise ValueError("Inputs to backups must be percentages")
                    if float(values[i]) < 0 or float(values[i]) > 100:
                        raise ValueError("backup efficiency values must be greater than zero and less than 100")
            backupPercents = backupPercent_values

        elif values[0] == "daysBackup":
            values.pop(0)
            if values[0] == "None" or values[0] == "none":
                backupDays_values = None
            elif len(values) != len(backups):
                raise ValueError("backup days and backup efficiencies must be the same size")
            else:
                backupDays_values = [] 
                for i in range(0, len(values)):
                    try:
                        backupDays_values.append(float(values[i]))
                    except:
                        raise ValueError("Inputs to backups must be days")
                    if int(values[i]) < 0:
                        raise ValueError("days of backup be greater than zero")
            daysBackup = backupDays_values

        elif values[0] == "depBackup":
            values.pop(0)
            if values[0] == "None" or values[0] == "none":
                depBackup_values = None
            elif len(values) != len(backups):
                raise ValueError("backup days and backup efficiencies must be the same size")
            else:
                depBackup_values = [] 
                for i in range(0, len(values)):
                    try:
                        depBackup_values.append(int(values[i]))
                    except:
                        raise ValueError("Inputs to backups must be parameter indices")
                    if int(values[i]) < 0 or int(values[i]) > 9:
                        raise ValueError("indices must be between 0 and 10")
            depBackup = depBackup_values


    if paramTypes is not None and paramIndexes is not None:
        if len(paramTypes) != len(paramIndexes):
            raise ValueError("number of paramTypes and paramIndexes entries must be the same")
    if optimize:
        leg = infrastructures_v4.optimizeDecon(n0, p0, repair_factors, nLoss, tLoss, timeSpan, nRun, paramTypes,
                                             paramIndexes, infStoichFactor, printProgress, averaging, intervals, agent, seedValue, name, remediationFactor, contamination,
                                               maxPercent, orders, coeffs, ks)
    else:
        leg = infrastructures_v4.infrastructures(n0, p0, repair_factors, nLoss, tLoss, timeSpan, nRun, paramTypes,
                                             paramIndexes, infStoichFactor, printProgress, averaging, intervals, agent, seedValue, name, remediationFactor, contamination,
                                                 backups, backupPercents, daysBackup, depBackup, orders, coeffs, ks)
##    leg = infrastructures_v4.infrastructures(n0, repair_factors, nLoss, tLoss, timeSpan, nRun, paramTypes,
##                                       paramIndexes, printProgress, averaging, intervals, seedValue)
    return leg

def read_file():

    #This function is only used by infrastructures_gui to prepopulate the entry boxes in the GUI

    #read file
    fname = "infrastructures_inputs.txt"
    with open(fname) as f:
        contents = f.readlines()

    #loop through each line and obtain the text for each entry
    for i in range(0, len(contents)):

        values = (contents[i]).split()

        if len(values) < 2:
            warnings.warn("Skipped line " +str(i)+ ", each input line must have at least two entries (a variable name and a value) in order to be entered")
            continue

        if values[0] == "n0":
            values.pop(0)
            n0String = ""
            for j in range(0, len(values)):
                if j == 0:
                    n0String = n0String + values[j]
                else:
                    n0String = n0String + " " + values[j]

        elif values[0] == "p0":
            values.pop(0)
            p0String = ""
            for j in range(0, len(values)):
                if j == 0:
                    p0String = p0String + values[j]
                else:
                    p0String = p0String + " " + values[j]

        elif values[0] == "repair_factors":
            values.pop(0)
            repair_factorsString = ""
            for j in range(0, len(values)):
                if j == 0:
                    repair_factorsString = repair_factorsString + values[j]
                else:
                    repair_factorsString = repair_factorsString + " " + values[j]

        elif values[0] == "nLoss":
            values.pop(0)
            nLossString = ""
            for j in range(0, len(values)):
                if j == 0:
                    nLossString = nLossString + values[j]
                else:
                    nLossString = nLossString + " " + values[j]

        elif values[0] == "tLoss":
            tLossString = values[1]

        elif values[0] == "timeSpan":
            timeSpanString = values[1]

        elif values[0] == "nRun":
            nRunString = values[1]

        elif values[0] == "paramTypes":
            values.pop(0)
            paramTypesString = ""
            for j in range(0, len(values)):
                if j == 0:
                    paramTypesString = paramTypesString + values[j]
                else:
                    paramTypesString = paramTypesString + " " + values[j]

        elif values[0] == "paramIndexes":
            values.pop(0)
            paramIndexesString = ""
            for j in range(0, len(values)):
                if j == 0:
                    paramIndexesString = paramIndexesString + values[j]
                else:
                    paramIndexesString = paramIndexesString + " " + values[j]

        elif values[0] == "printProgress":
            printProgressString = values[1]

        elif values[0] == "averaging":
            averagingString = values[1]

        elif values[0] == "infStoichFactor":
            infStoichFactorString = values[1]

        elif values[0] == "intervals":
            intervalsString = values[1]

        elif values[0] == "agent":
            agentString = values[1]

        elif values[0] == "seedValue":
            seedValueString = values[1]

        elif values[0] == "name":
            nameString = str(values[1])

        elif values[0] == "remediationFactor":
            values.pop(0)
            remediationString = ""
            for j in range(0, len(values)):
                if j == 0:
                    remediationString = remediationString + values[j]
                else:
                    remediationString = remediationString + " " + values[j]
            
        elif values[0] == "contamination":
            values.pop(0)
            contamString = ""
            for j in range(0, len(values)):
                if j == 0:
                    contamString = contamString + values[j]
                else:
                    contamString = contamString + " " + values[j]

        elif values[0] == "maxPercent":
            percentString = values[1]

        elif values[0] == "backups":
            values.pop(0)
            backupsString = ""
            for j in range(0, len(values)):
                if j == 0:
                    backupsString = backupsString + values[j]
                else:
                    backupsString = backupsString + " " + values[j]

        elif values[0] == "backupPercent":
            values.pop(0)
            backupPercentString = ""
            for j in range(0, len(values)):
                if j == 0:
                    backupPercentString = backupPercentString + values[j]
                else:
                    backupPercentString = backupPercentString + " " + values[j]
                    
        elif values[0] == "daysBackup":
            values.pop(0)
            daysBackupString = ""
            for j in range(0, len(values)):
                if j == 0:
                    daysBackupString = daysBackupString + values[j]
                else:
                    daysBackupString = daysBackupString + " " + values[j]

        elif values[0] == "depBackup":
            values.pop(0)
            depBackupString = ""
            for j in range(0, len(values)):
                if j == 0:
                    depBackupString = depBackupString + values[j]
                else:
                    depBackupString = depBackupString + " " + values[j]

    return n0String, p0String, repair_factorsString, nLossString, tLossString, timeSpanString, nRunString, paramTypesString, \
            paramIndexesString, printProgressString, averagingString, intervalsString, infStoichFactorString, agentString, \
            seedValueString, nameString, remediationString, contamString, percentString, backupsString, backupPercentString, daysBackupString, depBackupString
    #return n0String, repair_factorsString, nLossString, tLossString, timeSpanString, nRunString, paramTypesString,
           #paramIndexesString, printProgressString, averagingString, intervalsString, seedValueString

if __name__ == '__main__':
    leg = run_file()
