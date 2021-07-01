
from fpdf import FPDF
import PyPDF2
from PIL import Image
import os
import sys
import pandas as pd
import json
import pandas as pd
import numpy as np
import numpy
import os.path
import json
import locale
import matplotlib.pyplot as plt
from pathlib import Path
from plotnine import *
from matplotlib import rcParams
import pathlib
import subprocess
if (sys.version_info > (3, 0)):
  import tkinter as tk
  from tkinter import ttk
  from tkinter import *
else:
  import Tkinter as tk
  from Tkinter import ttl
import tkinter.messagebox as tkMessageBox
from pylab import *

#Root = os.path.abspath(os.path.dirname(__file__))
def avg(arr,token):
    count=0
    cat_count1=0
    cat_count2=0
    cat_count3=0
    cat_count4=0
    cat_count5=0
    cat_count6=0
    PreDecon=0
    PostDecon=0
    totalChar=0
    source=0
    Decon=0
    incident=0
    zeta=0
    if token=="days":
      for entry in arr:
        if zeta == 0:
            PreDecon=entry+PreDecon
            count=count+1
            cat_count1=cat_count1+1
            zeta=zeta+1

        elif zeta == 1:
            PostDecon=PostDecon+entry
            cat_count3=cat_count3+1
            count=count+1
            zeta=zeta+1
            
        elif zeta == 2:
            totalChar=totalChar+entry
            cat_count2=cat_count2+1
            count=count+1
            zeta=zeta+1
           
        elif zeta == 3 :
            source=source+entry
            cat_count4=cat_count4+1
            count=count+1
            zeta=zeta+1
        else:
            Decon=Decon+entry
            cat_count5=cat_count5+1
            count=count+1
            zeta=0
      PreDecon_avg=PreDecon/cat_count1
      PostDecon_avg=PostDecon/cat_count2
      totalChar_avg=totalChar/cat_count3
      source_avg=source/cat_count4
      Decon_avg=Decon/cat_count5
      averages=[]
      averages=[0 for i in range(5)]
      i=0
      for ind in averages:
          averages[i]=PreDecon_avg
          i=i+1
          averages[i]=PostDecon_avg
          i=i+1
          averages[i]=totalChar_avg
          i=i+1
          averages[i]=source_avg
          i=i+1
          averages[i]=Decon_avg
          break
      return averages
    else:
      for entry in arr:
        if zeta == 0:
            PreDecon=entry+PreDecon
            count=count+1
            cat_count1=cat_count1+1
            zeta=zeta+1

        elif zeta == 1:
            PostDecon=PostDecon+entry
            cat_count3=cat_count3+1
            count=count+1
            zeta=zeta+1
            
        elif zeta == 2:
            totalChar=totalChar+entry
            cat_count2=cat_count2+1
            count=count+1
            zeta=zeta+1
           
        elif zeta == 3 :
            source=source+entry
            cat_count4=cat_count4+1
            count=count+1
            zeta=zeta+1
        elif zeta==4:
            Decon=Decon+entry
            cat_count5=cat_count5+1
            count=count+1
            zeta=zeta+1
        else:
            incident=incident+entry
            cat_count6=cat_count6+1
            count=count+1
            zeta=0
      PreDecon_avg=PreDecon/cat_count1
      PostDecon_avg=PostDecon/cat_count2
      totalChar_avg=totalChar/cat_count3
      source_avg=source/cat_count4
      Decon_avg=Decon/cat_count5
      incident_avg=incident/cat_count6
      averages=[]
      averages=[0 for i in range(6)]
      i=0
      for ind in averages:
          averages[i]=PreDecon_avg
          i=i+1
          averages[i]=PostDecon_avg
          i=i+1
          averages[i]=totalChar_avg
          i=i+1
          averages[i]=source_avg
          i=i+1
          averages[i]=Decon_avg
          i=i+1
          averages[i]=incident_avg
          break
      return averages
def avgtotal(arr):
    count=0
    sum_total=0
    for entry in arr:
        if entry != 0:
            sum_total=entry+sum_total
            count=count+1
    avg=sum_total/count
    return avg
            
def createPdf(ranked_dict, ranked_dict_rt, filename, sensitivity, paramIndexes, paramTypes, n0, nRun, timeSpan, contamination, contaminated = False):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(204, 255, 204)
    width= 70
    height = 10
    pdf.set_font('Times', 'B', 16)
    pdf.cell(width, 5,filename + " SIRM Results", ln=1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height,"Introduction", ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.set_font('Times','', 12)
    introTextBlurb = "Large-scale chemical, biological, radiological, and nuclear (CBRN) incidents, whether a product of terrorism,"
    introTextBlurb2 = "war, or accidents, have the potential to damage core infrastructure assets."
    introTextBlurb3 = "In these situations, not only are directly affected areas not able to operate, but operations in other infrastructure "
    introTextBlurb4 = "sectors may not be able to operate without the services of the affected assets."
    pdf.cell(width, 5,introTextBlurb, ln=1)
    pdf.cell(width, 5,introTextBlurb2, ln=1)
    pdf.cell(width, 5,introTextBlurb3, ln=1)
    pdf.cell(width, 5,introTextBlurb4, ln=1)
    pdf.cell(width, 5, ln=1)
    introTextPt2 = "The Stochastic Infrastructure Remediation Model (SIRM) tool allows for a series of interconnected"
    introTextPt3 = "infrastructure sectors to be modeled and considers the realistic variability of the impact of a CBRN event."
    pdf.cell(width, 5,introTextPt2, ln=1)
    pdf.cell(width, 5,introTextPt3, ln=1)
    
    introText1 = "The results below for the {} scenario were produced by a Python tool that performs the SIRM calculations. ".format(filename)
    introText2 = "The SIRM's mechanics are based on the Gillespie Algorithm of stochastically modeling chemical kinetic systems, "
    introText3 = "with adjustments made to suit the modeling of infrastructure remediation after an event that incapacitates"
    introText3b = "infrastructure sectors (e.g. a CBRN event)."
    introText4 = "The SIRM examines the interactions of 9 different infrastructure sectors: Water, Energy, Transportation,"
    introText5 = "Communication, Government, Food/Agriculture, Emergency Services, Waste Management and Healthcare."
    introText6a = "Based on the initial operating efficiency after the event, the model calculates an estimated time"
    introText6b = "for recovery for each sector, averaged from a user-defined number of model runs ({}).".format(str(nRun))
    pdf.set_font('Times','', 12)
    pdf.cell(width, 5,introText2, ln=1)
    pdf.cell(width, 5,introText3, ln=1)
    pdf.cell(width, 5,introText3b, ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.cell(width, 5,introText4, ln=1)
    pdf.cell(width, 5,introText5, ln=1)
    pdf.cell(width, 5,introText6a, ln=1)
    pdf.cell(width, 5,introText6b, ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.cell(width, 5,introText1, ln=1)
    master_path = os.path.dirname(os.path.abspath('final_pdf.py'))
    Mapping_File_Path=Path("Results//Mapping.png")
    if Mapping_File_Path.exists():
        pdf.cell(width, height, "A map of the scenario is depicted below", ln=1)
        pdf.image("Results//Mapping.png", w=180)
    else:
        pdf.set_font('Times', '', 14)
        message="GIS data not available"
        pdf.cell(width, 5,message, ln=1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height,"Initial Inputs", ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.set_font('Times','', 12)
    introText7 = "The initial set of post-event infrastructure operating efficiencies input in the tool are displayed below:"
    pdf.cell(width, 5,introText7, ln=1)
    pdf.cell(width, 5, ln=1)
    sector_list = ["Water", "Energy", "Transportation", "Communications", "Government", "Food & Agriculture",
                   "Emergency Services", "Waste Management", "Healthcare"]
    data = ["Infrastructure Sector", "Initial Efficiency (%)", "Initial Contamination"]
    pdf.cell(60, height, str(data[0]), border=1, fill = True)
    pdf.cell(60, height, str(data[1]), border=1, fill = True)
    pdf.cell(60, height, str(data[2]), border=1, ln=1, fill = True)
    for i in range(len(n0)):
        pdf.cell(60, height, str(sector_list[i]), border=1)
        pdf.cell(60, height, str(n0[i]), border=1)
        if len(contamination) > 0:
            pdf.cell(60, height, str(round((100-contamination[i]),1)), border=1, ln=1)
        else:
            pdf.cell(60, height, str(0), border=1, ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.set_font('Times', 'B', 12)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, "The number and type of affected buildings/infrastructure :", ln=1)
    pdf.set_font('Times', '', 12)
    pdf.cell(width, 5, "Based on the map information, the tool produces a list of affected buildings/infrastructure. ", ln=1)
    pdf.cell(width, 5,"Some are affected by outages, while others may require decontamination.", ln=1)         
    pdf.set_font('Times', '', 12)
    pdf = getInfrastructureList("Contaminated//", pdf, width, 5, "Affected//", contaminated)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height,"Results", ln=1)
    pdf.cell(width, 2, ln=1)
    pdf.set_font('Times','', 12)
    pdf.cell(width, 5, 'The SIRM tool outputs the following set of results, which are provided in this report: \n', ln=1)
    pdf.cell(width, 5, '1) The suggested prioritization of sector remediation\n', ln=1)
    pdf.cell(width, 5, '2) Various charts of the results\n', ln=1)
    pdf.cell(width, 5, '3) Requested sensitivity analyses\n', ln=1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, 'Estimated Infrastructure Sector Prioritization Based on Strength of Infrastructure Connections: \n', ln=1)
    i = 1
    pdf.set_font('Times', '', 12)
    prior1 = "The first prioritization is based on how tightly linked an infrastructure is to other infrastructure sectors."
    prior2 = "The higher the connection strength, the more other infrastructure sectors are dependant on that infrastructure."
    prior3 = "Infrastructures with more dependancies will be prioritized in this ranking."
    data = ["Infrastructure Sector", "Connection Strength"] 
    pdf.cell(width, 5, prior1,ln=1)
    pdf.cell(width, 5, prior2,ln=1)
    pdf.cell(width, 5, prior3,ln=1)
    pdf.cell(width, height, str(data[0]), border=1,fill = True)
    pdf.cell(width, height, str(data[1]), border=1, ln=1, fill = True)
    for key, value in ranked_dict:
        data = [key, str(round(float(value), 2))]
        pdf.cell(width, height, str(data[0]), border=1)
        pdf.cell(width, height, str(data[1]), border=1, ln=1)
        i += 1
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, 'Estimated Infrastructure Prioritization Based on Median Recovery Time: \n', ln=1)
    i = 1
    pdf.set_font('Times', '', 12)
    prior1 = "The second prioritization is based to the average calculated recovery time in days for each sector."
    prior2 = "Infrastructures with longer average recovery times will be prioritized in this ranking."
    pdf.cell(width, 5, prior1,ln=1)
    pdf.cell(width, 5, prior2, ln=1)
    data = ["Infrastructure Sector", "Recovery Time (days)"]
    pdf.cell(width, height, str(data[0]), border=1, fill = True)
    pdf.cell(width, height, str(data[1]), border=1, ln=1, fill = True)
    for key, value in ranked_dict_rt:
        data = [key, str(round(float(value), 2))]
        pdf.cell(width, height, str(data[0]), border=1)
        pdf.cell(width, height, str(data[1]), border=1, ln=1)
        i += 1
    pdf.cell(width, height, ln=1)   
    #adding sensitivity
    graph = "Images/" + filename
    name = graph + ".png"
    
    #pdf.cell(width, height, "Sector Operating Efficiency over Time", ln=1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, "Graphical Output and Interpretation", ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.set_font('Times', '', 12)
    prior1 = "The graphs below represent requested outputs for various infrastructure sectors. The first graph charts the "
    prior2 = "efficiency of each sector over time."
    pdf.cell(width, 5, prior1,ln=1)
    pdf.cell(width, 5, prior2,ln=1)
    pdf.image(name, w=150)
    pdf.cell(width, 5, "The following charts were also requested by the user of the tool.",ln=1)
    if len(paramIndexes) < 1:
        pdf.cell(width, height, "No charts were requested by the SIRM tool user", ln=1)
    for i in range(len(paramIndexes)):
        sector_name = getSector(paramIndexes[i])
        graph = "Images/" + filename + " " + sector_name
        name = graph + ".png"
        pdf.image(name, w=150)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, "Requested Sensitivity Analyses", ln=1)
    pdf.set_font('Times', '', 12)
    pdf.cell(width, 5, "The user also has the option of running sensitivity analyses on various inputs in the tool. The results of the requested", ln=1)
    pdf.cell(width, 5, "sensitivity analyses are below.", ln=1)
    pdf.cell(width, 5, ln=1)
    if len(sensitivity) < 1:
        pdf.set_font('Times', '', 12)
        pdf.cell(width, height, "No sensitivity analyses were requested by the user", ln=1)

    pdf.set_font('Times', 'B', 12)
    for g in range(len(sensitivity)):
        graph = "Sensitivity Images/" + getSector(sensitivity[g]) + " Sensitivity43316916.png"
        pdf.image(graph, w=150)
    json_path="check.json"
    file = pathlib.Path(json_path)
    if file.exists() :
          with open(json_path) as f:
            data=json.load(f)
            check=data["check"]
    else:
        print ("File 'check.json' does not exist, please check directory for the file")
    with open(json_path) as f:
        data=json.load(f)
    check=data["check"]
    if check == "True" :
        days={}
        json_days='day.json'
        real=open("C:\\locations\\Realizethelocation.txt","w")
        real.write(master_path)
        real.close()
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        f = open("C:\\locations\\assemble.txt", "r")
        execute1=f.read()
        f.close()
        execute=execute1+"\Battelle.EPA.WideAreaDecon.Launcher.exe"
        fileLoc = master_path+"\\JobRequest.json"
        f=open(fileLoc)
        task5json=json.load(f)
        fileLoc = r'C:\Users\TYRAWA\Documents\SIRMResults.json'
        f=open(fileLoc)
        SIRM=json.load(f)
        Spore_loading=open(master_path+"\\SPORE.txt","r")
        Spore=Spore_loading.read()
        Spore_loading.close()
        spore_count=0
        Indoor_Spore=""
        Outdoor_Spore=""
        Underground_Spore=""
        Spore_Results=[]
        Spore_Results=[0 for i in range(len(Spore))]
        i=0
        b=0
        j=1
        for c in Spore:
            Spore_Results[i]=c
            i=i+1
        for z in Spore_Results:
           if z.isspace():
             spore_count=spore_count+1
           else:
             if spore_count==0:
               Indoor_Spore=Indoor_Spore+z
             elif spore_count==1:
               Outdoor_Spore=Outdoor_Spore+z
             elif spore_count==2:
               Underground_Spore=Underground_Spore+z

       
        task5json["defineScenario"]["filters"][0]["parameters"][0]["values"]["Indoor"]["value"]=SIRM["data"][6]["value"]##AREA CONTAMINATED
        task5json["defineScenario"]["filters"][0]["parameters"][0]["values"]["Outdoor"]["value"]=SIRM["data"][7]["value"]

        task5json["defineScenario"]["filters"][0]["parameters"][1]["values"]["Outdoor"]["value"]=Outdoor_Spore##LOADING
        task5json["defineScenario"]["filters"][0]["parameters"][1]["values"]["Underground"]["value"]=Underground_Spore
        task5json["defineScenario"]["filters"][0]["parameters"][1]["values"]["Indoor"]["value"]=Indoor_Spore

        task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Commercial"]["value"]=SIRM["data"][1]["value"]
        task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Industrial"]["value"]=SIRM["data"][0]["value"]
        task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Agricultural"]["value"]=SIRM["data"][5]["value"]
        task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Religious"]["value"]=SIRM["data"][2]["value"]
        task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Government"]["value"]=SIRM["data"][4]["value"]
        task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Educational"]["value"]=SIRM["data"][3]["value"]

       

##        #subprocess.call( execute ,check, startupinfo=si) #### CHECK HERE
        real=open(master_path+"\\realizations.txt","r")
        number=real.read()
        real.close()
        task5json["numberRealizations"]=number
        with open('newJobRequest.json', 'w') as myfile:
            json.dump(task5json,myfile)
        _path=master_path+"\\newJobRequest.json"
        result = subprocess.run([execute,_path],startupinfo=si)
 
        with open(execute1 + "\\Task 2 Results.json") as f: ## CHECK HERE
            task2=json.load(f)
        numrealization=len(task2)
        indexjson=numrealization-1
        z=0
        while z != numrealization:
            pdf.set_font('Times', 'B', 12)
            pdf.set_fill_color(204, 255, 204)
            height=10
            width= 70
            heading=[0 for i in range(7)]
            if z == 0:
                index=0
                index2=0
                index3=0
                indexkey=0
                Outdoor_phase_costs=[]
                Outdoor_phase_costs=[0 for i in range(6*numrealization)]
                Outdoor_workDays=[]
                Outdoor_workDays=[0 for i in range(5*numrealization)]
                Outdoor_total=[]
                Outdoor_total=[0 for i in range(1*numrealization)]
                
            for key in task2[z]["Outdoor"]:
                for key2 in task2[z]["Outdoor"][key]:
                    if key2 == "phaseCost":   
                       Outdoor_phase_costs[index]=task2[z]["Outdoor"][key][key2]
                       index=index+1
                    elif key2 == "workDays":
                       Outdoor_workDays[index2]=task2[z]["Outdoor"][key][key2]
                       
                       index2=index2+1
                    elif key2 == "totalCost":
                       Outdoor_total[index3]=task2[z]["Outdoor"][key][key2]
                       index3=index3+1
            if (z==indexjson):
                days["Outdoor"]=Outdoor_workDays
                some_text="The following data was generated by the Wide Area Decontamination Tool for the Indoor,Outdoor and Underground Catagories."
                text4="The metrics of average total cost for each type are located in the tables below."
                
                pdf.ln(" ")
                pdf.ln(" ")
                pdf.ln(" ")
                pdf.ln(" ")
                pdf.ln(" ")
                pdf.ln(" ")
                pdf.ln(" ")
                pdf.ln(" ")
                pdf.ln(" ")
                pdf.set_font('Times','B',16)
                pdf.cell(60,5, "Wide Area Decontamination Tool", ln=1)
                pdf.ln(" ")
                pdf.set_font('Times', '', 12)
                pdf.cell(60,5,some_text,ln=1)
                pdf.cell(60,5,text4,ln=1)
               
                pdf.ln(" ")
                pdf.ln(" ")
                
                text="Outdoor Results"
                pdf.set_font('Times','B',16)
                pdf.cell(60,5,text,ln=1)
                pdf.ln(" ")
                pdf.set_font('Times', '', 12)
                outdoor_avgs_money=avg(Outdoor_phase_costs,"money")
                outdoor_avgs_days=avg(Outdoor_workDays,"days")
                outdoor_avg_total=avgtotal(Outdoor_total)
                Titles = ["Phase", "Avg Phase Cost in USD","Avg Work Days"]      
                pdf.cell(90,height,Titles[0],border=1,fill=True)
                pdf.cell(50,height,Titles[1],border=1,fill=True)
                pdf.cell(45,height,Titles[2],border=1,fill=True)
                multi21=3
                heading=["Pre-Decontamination Characterization Sampling", "Post-Decontamination Characterization Sampling","Total Characterization Sampling","Source Reduction","Decontamination" ,"Incident Command"]
                for i in range(len(outdoor_avgs_money)):   
                    if multi21==3:
                        pdf.ln(" ")
                        multi21=0
                    else:
                        pdf.cell(90, height, str(heading[i-1]), border=1)
                        temp=outdoor_avgs_money[i-1]
                        temp=round(float(temp), 2)
                        temp="{0:,.2f}".format(temp)
                        pdf.cell(50,height,"$"+str(temp),border=1)
                        pdf.multi_cell(45, height, str(round(float(outdoor_avgs_days[i-1]), 2)), border=1)

                pdf.cell(90, height, str(heading[5]), border=1)
                temp=outdoor_avgs_money[5]
                temp=round(float(temp), 2)
                temp="{0:,.2f}".format(temp)
                pdf.cell(50,height,"$"+str(temp),border=1)
                pdf.multi_cell(45, height, str(round(float(0), 2)), border=1)
                pdf.ln(" ")
                disp=outdoor_avg_total
                disp=round(float(disp), 2)
                disp="{0:,.2f}".format(disp)
                text_45="The total outdoor cost was found from the Wide Area Decontamination Tool to be: $" + str(disp)
                pdf.cell(60,5,text_45,ln=1)
            if z == 0:
                index4=0
                index5=0
                index6=0
                Underground_phase_costs=[]
                Underground_phase_costs=[0 for i in range(6*numrealization)]
                Underground_workDays=[]
                Underground_workDays=[0 for i in range(5*numrealization)]
                Underground_total=[]
                Underground_total=[0 for i in range(1*numrealization)]
            for key in task2[z]["Underground"]:
                for key2 in task2[z]["Underground"][key]:
                    if key2 == "phaseCost":   
                       Underground_phase_costs[index4]=task2[z]["Underground"][key][key2]
                       index4=index4+1
                    elif key2 == "workDays":
                       Underground_workDays[index5]=task2[z]["Underground"][key][key2]
                       index5=index5+1
                    elif key2 == "totalCost":
                       Underground_total[index6]=task2[z]["Underground"][key][key2]
                       index6=index6+1
            if (z==indexjson):
                pdf.ln(" ")
                text="Underground Results"
                pdf.set_font('Times','B',16)
                pdf.cell(60,5,text,ln=1)
                pdf.set_font('Times', '', 12)
                pdf.ln(" ")
                days["Underground"]=Underground_workDays
                
                Underground_avgs_money=avg(Underground_phase_costs,"money")
                Underground_avgs_days=avg(Underground_workDays,"days")
                Underground_avg_total=avgtotal(Underground_total)
                heading=[0 for i in range(3)]
                heading=["Pre-Decontamination Characterization Sampling", "Post-Decontamination Characterization Sampling","Total Characterization Sampling","Source Reduction","Decontamination" ,"Incident Command"]
                Titles = ["Phase", "Avg Phase Cost in USD","Avg Work Days"]      
                pdf.cell(90,height,Titles[0],border=1,fill=True)
                pdf.cell(50,height,Titles[1],border=1,fill=True)
                pdf.cell(45,height,Titles[2],border=1,fill=True)
                multi21=3
                for i in range(len(Underground_avgs_money)):   
                    if multi21==3:
                        pdf.ln(" ")
                        multi21=0
                    else:
                        pdf.cell(90, height, str(heading[i-1]), border=1)
                        temp=Underground_avgs_money[i-1]
                        temp=round(float(temp), 2)
                        temp="{0:,.2f}".format(temp)
                        pdf.cell(50,height,"$"+str(temp),border=1)
                        pdf.multi_cell(45, height, str(round(float(Underground_avgs_days[i-1]), 2)), border=1)

                pdf.cell(90, height, str(heading[5]), border=1)
                temp=Underground_avgs_money[5]
                temp=round(float(temp), 2)
                temp="{0:,.2f}".format(temp)
                pdf.cell(50,height,"$"+str(temp),border=1)
                pdf.multi_cell(45, height, str(round(float(0), 2)), border=1)
                
                pdf.ln(" ")
                disp=Underground_avg_total
                disp=round(float(disp), 2)
                disp="{0:,.2f}".format(disp)
                text_45="The total indoor cost was found from the Wide Area Decontamination Tool to be: $" + str(disp)
                pdf.cell(60,5,text_45,ln=1)
                pdf.ln(" ")
            #########################Outdoor End
            if(z==0): 
                index8=0
                index9=0
                index10=0
                index11=0
                Indoor_types=[]
                Indoor_types=[0 for i in range(10*numrealization)]
                Indoor_phase_costs=[]
                Indoor_phase_costs=[0 for i in range(24*numrealization)]
                Indoor_workDays=[]
                Indoor_workDays=[0 for i in range(20*numrealization)]
                Indoor_total=[]
                Indoor_total=[0 for i in range(7*numrealization)]
            for key in task2[z]["Indoor"]:
                Indoor_types[index8] = key
                index8=index8+1
                for key2 in task2[0]["Indoor"][key]:
                    for key3 in task2[z]["Indoor"][key][key2]:
                        if key3 == "phaseCost":   
                           Indoor_phase_costs[index9]=task2[z]["Indoor"][key][key2][key3]
                           index9=index9+1
                        elif key3 == "workDays":
                           Indoor_workDays[index10]=task2[z]["Indoor"][key][key2][key3]
                           index10=index10+1
                        elif key3 == "totalCost":
                           Indoor_total[index11]=task2[z]["Indoor"][key][key2][key3]
                           index11=index11+1
            if (z==indexjson):
                pdf.ln(" ")
                with open(json_days, "w") as f:
                      json.dump(days,  f)

                pdf.ln(" ")
                pdf.ln(" ")
                pdf.ln(" ")
                pdf.ln(" ")
                pdf.ln(" ")
                pdf.ln(" ")
                text="Indoor Results"
                
                pdf.set_font('Times','B',16)
                
                pdf.cell(60,5,text,ln=1)
                pdf.ln(" ")
                pdf.set_font('Times', '', 12)
                text="The indoor results include inputs from Residential, Commercial, Industrial, Agricultural, Religous, Government,"
                text2="and Educational buildings. Phase costs and work days were taken from each type of building and averages for"
                text3="each phase were calculated and phase were calculated and displayed."
                pdf.cell(60,5,text,ln=1)
                pdf.cell(60,5,text2,ln=1)
                pdf.cell(60,5,text3,ln=1)
                
                indoor_avgs_money=avg(Indoor_phase_costs,"money")
                indoor_avgs_days=avg(Indoor_workDays,"days")
                indoor_avg_total=avgtotal(Indoor_total)
                
                heading=[0 for i in range(3)]
                pdf.ln(" ")
                Titles = ["Phase", "Avg Phase Cost in USD","Avg Work Days"]      
                pdf.cell(90,height,Titles[0],border=1,fill=True)
                pdf.cell(50,height,Titles[1],border=1,fill=True)
                pdf.cell(45,height,Titles[2],border=1,fill=True)
                multi21=3
                heading=[0 for i in range(6)]
                heading=["Pre-Decontamination Characterization Sampling", "Post-Decontamination Characterization Sampling","Total Characterization Sampling","Source Reduction","Decontamination" ,"Incident Command"]
                for i in range(len(indoor_avgs_money)):    
                    if multi21==3:
                        pdf.ln(" ")
                        multi21=0    
                    else:
                        pdf.cell(90, height, str(heading[i-1]), border=1)
                        temp=indoor_avgs_money[i-1]
                        temp="{0:,.2f}".format(temp)
                        pdf.cell(50,height,"$"+str(temp),border=1)
                        pdf.multi_cell(45, height, str(round(float(indoor_avgs_days[i-1]), 2)), border=1)


                pdf.cell(90, height, str(heading[5]), border=1)
                temp=indoor_avgs_money[5]
                temp="{0:,.2f}".format(temp)
                pdf.cell(50,height,"$"+str(temp),border=1)
                pdf.multi_cell(45, height, str(round(float(0), 2)), border=1)
                pdf.ln(" ")
                disp=indoor_avg_total
                disp=round(float(disp), 2)
                disp="{0:,.2f}".format(disp)
                text_45="The total indoor cost was found from the Wide Area Decontamination Tool to be: $" + str(disp)
                pdf.cell(60,5,text_45,ln=1)
                percent=[]
                percent=[0 for i in range(8)]
                percent[0]=task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Residential"]["value"]
                percent[1]=task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Commercial"]["value"]  
                percent[2]=task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Industrial"]["value"]
                percent[3]=task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Agricultural"]["value"]
                percent[4]=task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Religious"]["value"]
                percent[5]=task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Government"]["value"]
                percent[6]=task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Educational"]["value"]
                headings=[]
                headings=[0 for i in range(8)]
                headings=["Residential","Commercial","Industrial","Agricultural","Religious","Government","Educational"]
                fig, ax = plt.subplots()
                fig.set_size_inches(4, 4)
                colors1 = iter([plt.cm.Pastel1(i) for i in range(20)])
                newvalues = [x for x in percent if x != 0]
                plt.pie(newvalues, autopct='%1.1f%%',
                        shadow=True, startangle=90,colors=colors1)
                lgd=plt.legend(headings, bbox_to_anchor = (1.05, 0.6))
                plt.savefig('Indoor_Contamination%.png', bbox_extra_artists=(lgd,), bbox_inches="tight")
                pdf.image('Indoor_Contamination%.png', x = None, y = None, w=0, h=0, type='', link='')
                pdf.ln(" ")

            z=z+1
       
    else:
        
            print("")
            
    disclaimer1 = "Disclaimer: The results produced here are estimates and created through the use of the SIRM model."
    disclaimer1b = "the tool doesn’t account for auxiliary infrastructure such as power lines, water pipes, etc."
    disclamer1c = "that may impact operations/recovery."
    disclaimer2 = "Point of Contact: Timothy Boe, EPA, Timothy.Boe@epa.gov"
    pdf.cell(width, height,disclaimer1, ln=1)
    pdf.cell(width, height,disclaimer2, ln=1)
    path=Path(master_path + '\path.txt')
    if (path.exists()):
        f = open(path, "r")
        zeta=f.read()
        itter_path=zeta
        zeta=Path(zeta)
        if (zeta.exists()):
            b=0
            j=0
            check=False
            for i in reversed(itter_path):
                if i=='f' or i == 'p' or i == 'd' or i=='.' and b != 4:
                    b=b+1
                if (b==4):
                    check=True
                    break
                elif(j==4):
                    check=False
                    break
                else:
                    j=j+1
           
            if check==True and os.path.getsize(master_path + '\path.txt') != 0: ### path
                try:
                    pdf.output(itter_path)
                    tkMessageBox.showinfo("Helper","pdf created in the location provided: " + itter_path)
                except:
                    tkMessageBox.showinfo("Helper","Something went wrong check permissions for the filepath if not try entering new file path, no pdf created ")
            elif os.path.getsize(master_path + '\path.txt') != 0: #####path
                try:
                    pdf.output(itter_path + "\created.pdf" , 'F')
                    tkMessageBox.showinfo("Helper","pdf created in the location provided: " + itter_path +" with name created.pdf" )
                except:
                    tkMessageBox.showinfo("Helper","Something went wrong check permissions for the filepath if not try entering new file path, no pdf created")
            else:
                tkMessageBox.showinfo("Helper","no path provided Report is located in Results/" + filename + "_Report.pdf")
                pdf.output('Results/' + filename + "_Report.pdf", 'F')
        else:
            tkMessageBox.showinfo("Helper","your filepath is not valid and/or does not exists review your input and try again check the help button for a file path example report is generated in in Results/"+ filename + "_Report.pdf")
            pdf.output('Results/' + filename + "_Report.pdf", 'F')
    else:
        pdf.output('Results/' + filename + "_Report.pdf", 'F')

def getInfrastructureList(location, pdf, width, height, location2, contaminated, location3 = "Overall//"):
    data ={"Building Type": [], "Number of Contaminated buildings/infrastructure": []}
    dataAffected ={"Building Type": [], "Number of Affected buildings/infrastructure": []}
    dataOverall = {"Building Type": [], "Total number of buildings/infrastructure": []}
    tempresults = pd.DataFrame(data)
    tempresults2 = pd.DataFrame(dataAffected)
    tempresults3 = pd.DataFrame(dataOverall)
    pdf.cell(width, 5,ln=1)
    pdf.cell(width, height, "Number of buildings/infrastructure requiring decontamination:", ln=1)
    if contaminated:
        for filename in os.listdir(location):
            if filename.endswith(".csv") and "contaminated" in filename:
                filenames = filename.split("_c")
                building_type = filenames[0]
                building_type = building_type.split("_")
                building_type = ' '.join(building_type)
                results = pd.read_csv(os.path.join(location, filename))
                text = "{} : {}".format(str(building_type).capitalize(),
                                        str(len(results)))
                pdf.cell(width, height, text, ln=1)
                if len(results)>0:
                    new_row = {"Building Type": str(building_type).capitalize(), "Number of Contaminated buildings/infrastructure":len(results)}
                    tempresults = tempresults.append(new_row, ignore_index=True)
    pdf.cell(width, height, ln=1)
    pdf.cell(width, height, "Number of affected buildings/infrastructure:", ln=1)
    for filename in os.listdir(location2):
        if filename.endswith(".csv") and "contaminated" in filename:
            filenames = filename.split("_c")
            building_type = filenames[0]
            building_type = building_type.split("_")
            building_type = ' '.join(building_type)
            results = pd.read_csv(os.path.join(location2, filename))
            text = "{} : {}".format(str(building_type).capitalize(),
                                    str(len(results)))
            pdf.cell(width, height, text, ln=1)
            if len(results)>0:
                new_row = {"Building Type": str(building_type).capitalize(), "Number of Affected buildings/infrastructure":len(results)}
                tempresults2 = tempresults2.append(new_row, ignore_index=True)
    pdf.cell(width, height, ln=1)
    pdf.cell(width, height, "Total buildings/infrastructure in area:", ln=1)
    for filename in os.listdir(location3):
        if filename.endswith(".csv") and "contaminated" in filename:
            filenames = filename.split("_c")
            building_type = filenames[0]
            building_type = building_type.split("_")
            building_type = ' '.join(building_type)
            results = pd.read_csv(os.path.join(location3, filename))
            text = "{} : {}".format(str(building_type).capitalize(),
                                    str(len(results)))
            pdf.cell(width, height, text, ln=1)
            if len(results)>0:
                new_row = {"Building Type": str(building_type).capitalize(), "Total number of buildings/infrastructure":len(results)}
                tempresults3 = tempresults3.append(new_row, ignore_index=True)
    fig1, ax1 = plt.subplots()
    #print(tempresults)
    #patches, texts, autotexts = ax1.pie(tempresults["Number of Buildings"], labels=tempresults["Building Type"],
            #autopct = autopct_format(tempresults["Number of Buildings"]), startangle=90, pctdistance=0.85, labeldistance=1.2)
    ax1.axis('equal')
    #plt.style.use('ggplot')
    if contaminated and len(tempresults) > 0:
        result = pd.merge(tempresults, tempresults2, on="Building Type")
        finalresult = pd.merge(tempresults3, result, on="Building Type")
    else:
        finalresult = pd.merge(tempresults3, tempresults2, on="Building Type")
    #p = ggplot(finalresult, aes(x='Building Type', y='Number of Contaminated Buildings',fill = 'Building Type'))+ geom_col() + geom_col(aes(y='Number of Affected Buildings',x = 'Building Type', fill = 'Building Type')) + geom_col(aes(y='Number of Buildings', x = 'Building Type', fill = 'Building Type'))
    
    font = {'family' : 'normal',
        'size'   : 10}
    plt.rc('font', **font)
    
    p = finalresult.groupby('Building Type').mean().plot(kind='bar')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    plt.xticks(rotation = -45, fontsize=8)
    plt.tight_layout()
    rcParams.update({'figure.autolayout': True})
    p.get_figure().savefig('ColumnChart.png')
    pdf.image(dir_path+"\\ColumnChart.png", w=200)
    return pdf

    
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_format

def getSector(index):
    if index == 0:
        return "Water"
    elif index == 1:
        return "Energy"
    elif index == 2:
        return "Transportation"
    elif index == 3:
        return "Communication"
    elif index == 4:
        return "Government"
    elif index == 5:
        return "Food"
    elif index == 6:
        return "Emergency Services"
    elif index == 7:
        return "Waste"
    else:
        return "Healthcare"
    
