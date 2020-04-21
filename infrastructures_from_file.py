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
import tkinter.messagebox as tkMessageBox
import json

def run_file(optimize, orders, coeffs, ks):

    #defaults
    n0 = [100,50,100,100,100,100,100,100, 100]
    p0 = [699900, 100, 0, 0]
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
    remediationFactor = [1,1,1,1,1,1,1,1,1]
    contamination = [0,0,0,0,0,0,0,0,0]

    #read file
    fname = "infrastructure_inputs.json"
    json_data = open(fname)
    data = json.load(json_data)
    
    #n0 calculation
    n_values = list(data["n0"])
    if check_inputs("n0", n_values, 100, 0, 9):
        n0 = np.zeros(9,dtype=int)
        for i in range(0, len(n_values)):
            try:
                n0[i] = float(n_values[i])
            except:
                tkMessageBox.showerror("Error","Inputs to n0 must be float/decimal values")
                raise ValueError("Inputs to n0 must be float/decimal values")
    #reading p0            
    p_values = list(data["p0"])
    if check_inputs("p0", p_values, 1E50, 0, 4):
        p0 = np.zeros(4,dtype=int)
        for i in range(0, len(p_values)):
            try:
                p0[i] = int(p_values[i])
            except:
                tkMessageBox.showerror("Error","Inputs to p0 must be integer values")
                raise ValueError("Inputs to p0 must be integer values")
    #reading repair_factors
    
    rf_values = list(data["repair_factors"])
    if rf_values[0] == "None":
        repair_factors = None
    elif check_inputs("rf_values", rf_values, 100, 0, 9):
        repair_factors = np.zeros(9,dtype=float)
        for i in range(0, len(repair_factors)):
            try:
                repair_factors[i] = float(rf_values[i])
            except:
                tkMessageBox.showerror("Error","Inputs to repair_factors must be float/decimal values")
                raise ValueError("Inputs to repair_factors must be float/decimal values")

    
    nLoss_vals = data["nLoss"]
    if nLoss_vals == "None" or nLoss_vals == "none":
        nLoss = None
        tLoss = None
    elif check_inputs("nLoss_vals", n_values, 100, 0, 9):
        nLoss = np.zeros(9,dtype=float)
        for i in range(0, len(list(nLoss_vals))):
            try:
                nLoss = float(nLoss_vals)
            except:
                tkMessageBox.showerror("Error","Inputs to nLoss must be float/decimal values")
                raise ValueError("Inputs to nLoss must be float/decimal values")
    if nLoss is None or nLoss == (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0):
        tLoss = None

    tLoss_vals = data["tLoss"]
    if tLoss_vals == "none" or tLoss_vals == "None" or tLoss_vals == "0":
        tLoss = None
        nLoss = None
    elif check_single_input("tLoss", tLoss_vals, 1E50, 0):
        tLoss = float(tLoss_vals)
            
    if check_single_input("timeSpan", data["timeSpan"], 1E50, 0):
        timeSpan = float(data["timeSpan"])


    try:
        nRun = int(data["nRun"])
    except:
        tkMessageBox.showerror("Error","Input to nRun must be an integer")
        raise TypeError("Input to nRun must be an integer")
    if nRun < 1:
        tkMessageBox.showerror("Error","nRun must be an integer 1 or greater")
        raise ValueError("nRun must be an integer 1 or greater")

    pt_values = list(data["paramTypes"])
    paramTypes = []
    if pt_values[0] == "None" or pt_values[0] == "none":
        paramTypes = None
        paramIndexes = None
    else:
        for i in range(0, len(pt_values)):
            if pt_values[i] != "min" and pt_values[i] != "max" and pt_values[i] != "average" and pt_values[i] != "final_val" and pt_values[i] != "rt":
                tkMessageBox.showerror("Error","Unknown parameter type, acceptable values are 'min', 'max', 'average', 'rt', and 'final_val'")
                raise ValueError("Unknown parameter type, acceptable values are 'min', 'max', 'average', 'rt', and 'final_val'")
            else:
                paramTypes.append(pt_values[i])

    pi_values = list(data["paramIndexes"])
    paramIndexes = []
    if pi_values[0] == "None" or pi_values[0] == "none":
        paramTypes = None
        paramIndexes = None
    else:
        if check_inputs("paramIndexes", pi_values, 9, 0, len(paramTypes)):    
            for i in range(0, len(pi_values)):
                try:
                    paramIndexes.append(int(pi_values[i]))
                except:
                    tkMessageBox.showerror("Error","Inputs to paramIndexes must be integers")
                    raise ValueError("Inputs to paramIndexes must be integers")

    infStoichFactor_val = data["infStoichFactor"]
    infStoichFactor = None
    if infStoichFactor == "None":
        infStoichFactor = None
    else:
        try:
            infStoichFactor = float(infStoichFactor_val)
        except:
            tkMessageBox.showerror("Error","infStoichFactor must be a float/decimal value")
            raise TypeError("infStoichFactor must be a float/decimal value")


    printProgress = data["printProgress"]
    if printProgress == "True":
        printProgress = True
    else:
        printProgress = False

    averaging = data["averaging"]
    if averaging == "True":
        averaging = True
    else:
        averaging = False

    intervals = data["intervals"]
    if intervals == "True":
        intervals = True
    else:
        intervals = False

    agent = data["agent"]
    if agent != "anthrax" and agent != "ebola" and agent != "monkeypox" and agent != "natural_disaster":
        tkMessageBox.showerror("Error","Unsupported Agent Name")
        raise ValueError("Unsupported Agent Name")

    seedValue = data["seedValue"]
    if seedValue == "none" or seedValue == "None" or seedValue == "false" or seedValue == "False":
        seedValue = None
    else:
        try:
            seedValue = int(seedValue)
        except:
            tkMessageBox.showerror("Error","seedValue input must be an integer or 'None'")
            raise TypeError("seedValue input must be an integer or 'None'")
    
    name = data["name"]
        
    remediationFactor_vals = list(data["remediationFactor"])
    remediationFactor = np.zeros(9,dtype=float)
    if check_inputs("remediationFactor", remediationFactor_vals, 100, 0, 9):
        for i in range(0, len(remediationFactor_vals)):
            try:
                remediationFactor[i] = float(remediationFactor_vals[i])
            except:
                tkMessageBox.showerror("Error","Inputs to n0 must be float/decimal values")
                raise ValueError("Inputs to n0 must be float/decimal values")
            
    c_values = list(data["contamination"])
    contamination = np.zeros(9,dtype=float)
    if check_inputs("contamination", c_values, 100, 0, 9):
        for i in range(0, len(c_values)):
            try:
                contamination[i] = 100-float(c_values[i])
            except:
                tkMessageBox.showerror("Error","Inputs to contamination must be float/decimal values")
                raise ValueError("Inputs to n0 must be float/decimal values")
                
    b_values = list(data["backups"])
    backups = []
    if b_values[0] == "None" or b_values[0] == "none":
        backups = None
    elif check_inputs("backups", b_values, 9, 0, len(b_values)):
        
        for i in range(0, len(b_values)):
            try:
                backups.append(int(b_values[i]))
            except:
                tkMessageBox.showerror("Error","Inputs to backups must be parameter indexes")
                raise ValueError("Inputs to backups must be parameter indexes")

    bp_values = list(data["backupPercent"])
    backupPercents = [] 
    if bp_values[0] == "None" or bp_values[0] == "none":
        backupPercents = None
    
    elif check_inputs("backupPercent", bp_values, 100, 0, len(backups)):
        for i in range(0, len(bp_values)):
            try:
                backupPercents.append(float(bp_values[i]))
            except:
                tkMessageBox.showerror("Error","Inputs to backupPercent must be percentages")
                raise ValueError("Inputs to backupPercent must be percentages")

    db_values = list(data["daysBackup"])
    daysBackup = []
    if db_values[0] == "None" or bp_values[0] == "none":
        daysBackup = None
     
    elif check_inputs("daysBackup", db_values, timeSpan, 0, len(backups)):
        for i in range(0, len(db_values)):
            try:
                daysBackup.append(float(db_values[i]))
            except:
                tkMessageBox.showerror("Error","Inputs to daysBackup must be floats")
                raise ValueError("Inputs to backupPercent_values must be floats")

    depb_values = list(data["depBackup"])
    depBackup = [] 
    if db_values[0] == "None" or depb_values[0] == "none":
        depBackup = None
    
    elif check_inputs("depBackup", depb_values, timeSpan, 0, len(backups)):
        for i in range(0, len(depb_values)):
            try:
                depBackup.append(float(depb_values[i]))
            except:
                tkMessageBox.showerror("Error","Inputs to depBackup must be percentages")
                raise ValueError("Inputs to depBackup must be percentages")

    neg_values = data["negatives"]
    if neg_values == "true" or neg_values == "True" or neg_values == "1":
        negatives = True
    else:
        negatives = False

    leg = infrastructures_v4.infrastructures(n0, p0, repair_factors, nLoss, tLoss, timeSpan, nRun, paramTypes,
                                             paramIndexes, infStoichFactor, printProgress, averaging, intervals, agent, seedValue, name, remediationFactor, contamination,
                                                 backups, backupPercents, daysBackup, depBackup, orders, coeffs, ks, negatives)
##    leg = infrastructures_v4.infrastructures(n0, repair_factors, nLoss, tLoss, timeSpan, nRun, paramTypes,
##                                       paramIndexes, printProgress, averaging, intervals, seedValue)
    return leg
    
def check_inputs(inputName, inputs, max, min, length):
    meetsLength = True
    if len(inputs) != length: 
        meetsLength = False
    meetsMin = all(float(i) >= min for i in inputs)
    meetsMax = all(float(i) <= max for i in inputs)
    lengthError = "length of " + inputName + " must be " + str(length)
    valueError = inputName + " values must be between" + str(min) + " and " + str(max)
    if meetsLength and meetsMin and meetsMax:
        return True
    else:
        if meetsLength:
            tkMessageBox.showerror("Error",valueError)
            raise TypeError(valueError)
        else:
            tkMessageBox.showerror("Error",lengthError)
            raise TypeError(lengthError)

def check_single_input(inputName, input, max, min):
    try:
        result = float(input)
    except:
        tkMessageBox.showerror("Error","Input to %s must be a float/decimal" % inputName)
        raise TypeError("Input to %s must be a float/decimal" % inputName)
        return False
    if float(input) <= min or float(input) >= max:
        tkMessageBox.showerror("Error","%s must be a float/decimal greater than %f and less than %f" % inputName, min, max)
        raise ValueError("%s must be a float/decimal greater than %f and less than %f" % inputName, min, max)
        return False
    return True
        
def read_file():

    #This function is only used by infrastructures_gui to prepopulate the entry boxes in the GUI

    #read file
    fname = "infrastructure_inputs.json"
    json_data = open(fname)
    data = json.load(json_data)
    
    n0String = data["n0"]
    p0String = data["p0"]
    repair_factorsString = data["repair_factors"]
    nLossString = data["nLoss"]
    tLossString = data["tLoss"]
    timeSpanString = data["timeSpan"]
    nRunString = data["nRun"]
    paramTypesString = data["paramTypes"]
    paramIndexesString = data["paramIndexes"]
    printProgressString = data["printProgress"]
    averagingString = data["averaging"]
    intervalsString = data["intervals"]
    infStoichFactorString = data["infStoichFactor"]
    agentString = data["agent"]
    seedValueString = data["seedValue"]
    nameString = data["name"]
    remediationString = data["remediationFactor"]
    contamString = data["contamination"]
    backupsString = data["backups"]
    backupPercentString = data["backupPercent"]
    daysBackupString = data["daysBackup"]
    depBackupString = data["depBackup"]
    negativesString = data["negatives"]
    

    return n0String, p0String, repair_factorsString, nLossString, tLossString, timeSpanString, nRunString, paramTypesString, \
            paramIndexesString, printProgressString, averagingString, intervalsString, infStoichFactorString, agentString, \
            seedValueString, nameString, remediationString, contamString, backupsString, backupPercentString, daysBackupString, depBackupString, \
            negativesString
    #return n0String, repair_factorsString, nLossString, tLossString, timeSpanString, nRunString, paramTypesString,
           #paramIndexesString, printProgressString, averagingString, intervalsString, seedValueString

if __name__ == '__main__':
    leg = run_file()
