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
    inputs = list(range(10))
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

def createbackupInputs(folder, inputFile, OutputPath):
    json_data = open(folder+"\\"+inputFile)
    data = json.load(json_data)
    efficiencies = [1,5,9]
    days = [1,5,10]
    indexes = [0,1]
    myInt = 10
    newList = [x * myInt for x in efficiencies]
    for i in range(len(efficiencies)):
        for j in range(len(indexes)):
            for k in range(len(days)):
                adjusted = data["n0"].copy()
                adjusted[indexes[j]] = newList[i]

                adjusted_data = data.copy()
                adjusted_data["repair_factors"] = [0.5]*9
                adjusted_data["backups"] = [indexes[j]]*8
                adjusted_data["backupPercent"] = [newList[i]]*8
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
