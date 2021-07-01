import os
from os.path import abspath
from inspect import getsourcefile
import json

def runSensitivity(repairRange, stoichFactor, n0Inputs, days, efficiencies, indexes):
    input_filename = "infrastructures_inputs.txt"
    dir_path = os.path.dirname(abspath(getsourcefile(lambda:0)))
    if not os.path.exists(dir_path+'\\Sensitivity'):
        os.makedirs(dir_path+'\\Sensitivity')
    if not os.path.exists(dir_path+'\\Sensitivity\\repairFactors'):
        os.makedirs(dir_path+'\\Sensitivity\\repairFactors')
    if not os.path.exists(dir_path+'\\Sensitivity\\n0'):
        os.makedirs(dir_path+'\\Sensitivity\\n0')
    if not os.path.exists(dir_path+'\\Sensitivity\\backup'):
        os.makedirs(dir_path+'\\Sensitivity\\backup')
    if not os.path.exists(dir_path+'\\Sensitivity\\infStoich'):
        os.makedirs(dir_path+'\\Sensitivity\\infStoich')
    createRepairFactorsInputs(dir_path, input_filename, dir_path + "//Sensitivity", repairRange)
    createInfInputs(dir_path, input_filename, dir_path + "//Sensitivity", stoichFactor)
    createn0Inputs(dir_path, input_filename, dir_path + "//Sensitivity", n0Inputs)
    createbackupInputs(dir_path, input_filename, dir_path + "//Sensitivity", days, efficiencies, indexes)

def createRepairFactorsInputs(folder, inputFile, OutputPath, inputs):
    json_data = open(folder+"\\"+inputFile)
    data = json.load(json_data)
    myInt = 10
    newList = [x / myInt for x in inputs]
    adjusted = [0.5]*9
    for i in range(len(adjusted)):
        for j in range(len(inputs)):
            adjusted = [0.5]*9
            adjusted[i] = newList[j]
            adjusted_data = data.copy()
            adjusted_data["repair_factors"] = adjusted
            fileName = str(i) + "_" + str(inputs[j])
            adjusted_data["name"] = fileName
            with open(OutputPath + "\\repairFactors\\" + fileName + ".txt", "w+") as outfile:
                json.dump(adjusted_data, outfile)

def createInfInputs(folder, inputFile, OutputPath, inputs):
    json_data = open(folder+"\\"+inputFile)
    data = json.load(json_data)
    myInt = 10
    newList = [x / myInt for x in inputs]
    for j in range(len(inputs)):
        fileName = str(inputs[j])
        adjusted_data = data.copy()
        adjusted_data["repair_factors"] = [0.5]*9
        adjusted_data["infStoichFactor"] = newList[j]
        adjusted_data["name"] = fileName
        with open(OutputPath + "\\infStoich\\" + fileName + ".txt", "w+") as outfile:
            json.dump(adjusted_data, outfile)
                
def createn0Inputs(folder, inputFile, OutputPath, inputs):
    json_data = open(folder+"\\"+inputFile)
    data = json.load(json_data)
    inputs = list(range(10))
    indexes = [7]
    myInt = 10
    newList = [x * myInt for x in inputs]
    for i in range(len(inputs)):
        for j in range(len(indexes)):
            adjusted = data["n0"].copy()
            adjusted[indexes[j]] = newList[i]
            
            adjusted_data = data.copy()
            adjusted_data["repair_factors"] = [0.5]*9
            adjusted_data["n0"] = adjusted
            fileName = str(i) + "_" + str(indexes[j])
            adjusted_data["name"] = fileName
            with open(OutputPath + "\\n0\\" + fileName + ".txt", "w+") as outfile:
                json.dump(adjusted_data, outfile)

def createbackupInputs(folder, inputFile, OutputPath, days, efficiencies, indexes):
    json_data = open(folder+"\\"+inputFile)
    data = json.load(json_data)
    myInt = 10
    for i in range(len(efficiencies)):
        for j in range(len(indexes)):
            for k in range(len(days)):
                adjusted = data["n0"].copy()
                adjusted[indexes[j]] = efficiencies[i]
                adjusted_data = data.copy()
                adjusted_data["repair_factors"] = [0.5]*9
                adjusted_data["backups"] = [indexes[j]]*8
                adjusted_data["backupPercent"] = [efficiencies[i]]*8
                adjusted_data["daysBackup"] = [days[k]]*8
                dep_params = list(range(indexes[j])) + list(range(indexes[j]+1, 9))
                adjusted_data["depBackup"] = dep_params
                fileName = str(indexes[j]) + "_" + str(efficiencies[i]) + "_" + str(days[k])
                adjusted_data["name"] = fileName
                with open(OutputPath + "\\backup\\" + fileName + ".txt", "w+") as outfile:
                    json.dump(adjusted_data, outfile)

def analyzen0(directory, n0_sector):
    n0 = []
    sector_n0 = []
    recovery_time_n0 = []
    
    for filename in os.listdir(directory):
        if (filename.endswith(".csv")):
            filename_fixed = filename.split(".")[0]
            categories = filename_fixed.split("_")
            repair_factors = [0.5]*9
            n0s = []
            infStoich = 1
            data = pd.read_csv(directory+ "\\" + filename)
            for i in range(len(data["Sectors"])):
                sector = data["Sectors"][i]
                recoveryTime = data["Recovery Times"][i]
                n0percentage = float(categories[0])*10
                n0.append(n0percentage)
                sector_n0.append(sector)                   
                recovery_time_n0.append(recoveryTime)
    n0HealthcareAnalysis = pd.DataFrame()
    n0HealthcareAnalysis["n0"] = n0
    n0HealthcareAnalysis["Sector"] = sector_n0
    n0HealthcareAnalysis["Recovery Time"] = recovery_time_n0
    n0HealthcareAnalysis.to_csv(directory + "\\Results\\n0Analysis.csv",index=False)

def analyzeRF(directory):
    RF_sectors = []
    RF_recovery_time = []
    RPSector = []
    RPValues = []
    for filename in os.listdir(directory):
        if (filename.endswith(".csv")):
            filename_fixed = filename.split(".")[0]
            categories = filename_fixed.split("_")
            repair_factors = [0.5]*9
            n0s = []
            infStoich = 1
            data = pd.read_csv(directory+ "\\" + filename)
            for i in range(len(data["Sectors"])):
                rp_sector = categories[0]
                RPValues.append(int(categories[1])/10)
                RPSector.append(rp_sector)
                RF_sectors.append(sector)
                RF_recovery_time.append(recoveryTime)
    repair_factorAnalysis = pd.DataFrame()
    repair_factorAnalysis["Sector"] = RF_sectors
    repair_factorAnalysis["Recovery Time"] = RF_recovery_time
    repair_factorAnalysis["Repair Factor Sector"] = RPSector
    repair_factorAnalysis["Repair Factor Value"] = RPValues
    repair_factorAnalysis.to_csv(directory + "\\Results\\rfAnalysis.csv",index=False)

def analyzeBackups(directory):
    sectors = []
    recovery_time = []
    backup_sector = []
    backup_days = []
    backup_efficiencies = []
    for filename in os.listdir(directory):
        if (filename.endswith(".csv")):
            filename_fixed = filename.split(".")[0]
            categories = filename_fixed.split("_")
            data = pd.read_csv(directory+ "\\" + filename)
            for i in range(len(data["Sectors"])):
                sectors.append(data["Sectors"][i])
                recovery_time.append(data["Recovery Times"][i])
                backup_sector.append(categories[0])
                backup_days.append(categories[2])
                e = float(categories[1])*10
                backup_efficiencies.append(e)
    analysis = pd.DataFrame()
    analysis["Sector"] = sectors
    analysis["Recovery Time"] = recovery_time
    analysis["Backup Sector"] = backup_sector
    analysis["Backup Efficiencies"] = backup_efficiencies
    analysis["Backup Days"] = backup_days
    analysis.to_csv(directory + "\\Results\\BackupAnalysis.csv",index=False)

def analyzeStoich(directory):
    infStoichFactors = []        
    sector_infStoichFactors = []
    recovery_time_infStoichFactors = []

    for filename in os.listdir(directory):

        if (filename.endswith(".csv")):
            filename_fixed = filename.split(".")[0]
            categories = filename_fixed.split("_")
            repair_factors = [0.5]*9
            n0s = []
            infStoich = 1
            data = pd.read_csv(directory+ "\\" + filename)
            for i in range(len(data["Sectors"])):
                sector = data["Sectors"][i]
                recoveryTime = data["Recovery Times"][i]
                infStoich = int(categories[0])
                sector_infStoichFactors.append(sector)                   
                recovery_time_infStoichFactors.append(recoveryTime)
                infStoichFactors.append(infStoich)
    infStoichFactorAnalysis = pd.DataFrame()
    infStoichFactorAnalysis["Sector"] = sector_infStoichFactors
    infStoichFactorAnalysis["Recovery Time"] = recovery_time_infStoichFactors
    infStoichFactorAnalysis["Inf Stoich Factor"] = infStoichFactors
    infStoichFactorAnalysis.to_csv(directory + "\\Results\\infStoichAnalysis.csv",index=False)
