# -*- coding: utf-8 -*-
"""
infrastructures_gui.py
Created on Sun Jun 25 14:23:05 2019
Created by: Mitchell Wendt
Revised: 08/28/2019
Revised by: Mitchell Wendt
"""

#import statements
import sys
if (sys.version_info > (3, 0)):
  import tkinter as tk
  from tkinter import ttk
  from tkinter import *
else:
  import Tkinter as tk
  from Tkinter import ttl
import infrastructures_from_file
import coefficients_from_file
import report_GUI
from shutil import copyfile
#import sensitivity_GUI
import tkinter.messagebox as tkMessageBox
#from fiona import _shim, schema
#import infrastructures_mapping
import json
from inspect import getsourcefile
from os.path import abspath
import matplotlib.pyplot as plt
#from Tkinter import Label
from tkinter import ttk
import subprocess
import os
#import geopandas
if (sys.version_info > (3,0)):
  from tkinter.filedialog import askopenfilename
else:
  from tkFileDialog import askopenfilename

if (sys.version_info > (3,0)):
  from tkinter.filedialog import asksaveasfile
else:
  from tkFileDialog import asksaveasfile



class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 480   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None
    
    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="alice blue", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
      

def main():
    LARGE_FONT= ("Courier New", 24)

    class TKinterWindow(tk.Tk):

        def __init__(self, *args, **kwargs):

            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)
            style=ttk.Style(self)
            self.tk.call('source','azure.tcl')
            style.theme_use('azure')
            container.pack(side="top", fill="both", expand = True)

            container.grid_rowconfigure(900, weight=1)
            #container.grid_columnconfigure(5, weight=1,minsize="600")

            self.frames = {}

            frame = StartPage(container, self)

            self.frames[StartPage] = frame

            frame.grid(row=1, column=1, sticky="nsew")
            frame.configure(bg="snow")
            #self.geometry("1200x750")
            
            

            self.show_frame(StartPage)

        def show_frame(self, cont):
            
            frame = self.frames[cont]
            #frame.config(bg="#F7FCF6")
            frame.tkraise()
        def appClose(self):
            print('main app close')
            self.destroy()
            sys.exit()
            self.quit()
            
    class StartPage(tk.Frame):

        def __init__(self, parent, controller):

            self.leg = None
            #dir_path = os.path.dirname(os.path.realpath(__file__))
            dir_path = os.path.dirname(abspath(getsourcefile(lambda:0)))
            dirpath = os.getcwd()
            self.orders, self.coeffs, self.k = coefficients_from_file.load_file(dir_path + "//"+ "default.csv")
            #print(self.orders, self.coeffs, self.k)

            def select_all():

              water_bool.set(True)
              water_graph_bool.set(True)
              energy_bool.set(True)
              energy_graph_bool.set(True)
              transportation_bool.set(True)
              transportation_graph_bool.set(True)
              comm_bool.set(True)
              comm_graph_bool.set(True)
              gov_bool.set(True)
              gov_graph_bool.set(True)
              emer_bool.set(True)
              emer_graph_bool.set(True)
              fa_bool.set(True)
              fa_graph_bool.set(True)
              waste_bool.set(True)
              waste_graph_bool.set(True)
              healthcare_bool.set(True)
              healthcare_graph_bool.set(True)
   
              

            def deselect_all():
              water_bool.set(False)
              water_graph_bool.set(False)
              energy_bool.set(False)
              energy_graph_bool.set(False)
              transportation_bool.set(False)
              transportation_graph_bool.set(False)
              comm_bool.set(False)
              comm_graph_bool.set(False)
              gov_bool.set(False)
              gov_graph_bool.set(False)
              emer_bool.set(False)
              emer_graph_bool.set(False)
              fa_bool.set(False)
              fa_graph_bool.set(False)
              waste_bool.set(False)
              waste_graph_bool.set(False)
              healthcare_bool.set(False)
              healthcare_graph_bool.set(False)
            def run(optimize):
                data = {}
                n0List = []
                n0List.append(waterVar.get())
                n0List.append(energyVar.get())
                n0List.append(transportVar.get()) 
                n0List.append(communicationsVar.get())
                n0List.append(governmentVar.get())
                n0List.append(agricultureVar.get())
                n0List.append(emerServVar.get())
                n0List.append(wasteVar.get())
                n0List.append(healthcareVar.get())
                data["n0"] = n0List
                #data["p0"] = var6.get().split(" ")
                data["repair_factors"] = var7.get().split(" ")
                data["nLoss"] = var8.get()
                data["tLoss"] = var9.get()
                data["timeSpan"] = var12.get()
                data["nRun"] = var10.get()
                data["paramTypes"] = var13.get().split(" ")
                data["paramIndexes"] = var14.get().split(" ")
                data["infStoichFactor"] = var15.get()
                data["printProgress"] = var1.get()
                data["averaging"] = var2.get()
                data["intervals"] = var3.get()
                #data["agent"] = var4.get()
                data["seedValue"] = var16.get()
                data["name"] = var17.get()
                data["remediationFactor"] = var18.get().split(" ")
                data["contamination"] = var19.get().split(" ")
                data["backups"] = var21.get().split(" ")
                data["backupPercent"] = var22.get().split(" ")
                data["daysBackup"] = var23.get().split(" ")
                data["depBackup"] = var24.get().split(" ")
                data["negatives"] = var25.get()
                fileLoc = dir_path + "//" + "infrastructures_inputs.txt"
                with open(fileLoc, "w") as outfile:
                    json.dump(data, outfile)
                data = {}
                data["water"]={}
                data["water"]["sensitivity"] = water_bool.get()
                data["water"]["graph"] = water_graph_bool.get()
                data["water"]["index"] = 0
                data["energy"]={}
                data["energy"]["sensitivity"] = energy_bool.get()
                data["energy"]["graph"] = energy_graph_bool.get()
                data["energy"]["index"] = 1
                data["transportation"]={}
                data["transportation"]["sensitivity"] = transportation_bool.get()
                data["transportation"]["graph"] = transportation_graph_bool.get()
                data["transportation"]["index"] = 2
                data["communications"]={}
                data["communications"]["sensitivity"] = comm_bool.get()
                data["communications"]["graph"] = comm_graph_bool.get()
                data["communications"]["index"] = 3
                data["gov"]={}
                data["gov"]["sensitivity"] = gov_bool.get()
                data["gov"]["graph"] = gov_graph_bool.get()
                data["gov"]["index"] = 3
                data["food"]={}
                data["food"]["sensitivity"] = fa_bool.get()
                data["food"]["graph"] = fa_graph_bool.get()
                data["food"]["index"] = 3
                data["emer"]={}
                data["emer"]["sensitivity"] = emer_bool.get()
                data["emer"]["graph"] = emer_graph_bool.get()
                data["emer"]["index"] = 3
                data["waste"]={}
                data["waste"]["sensitivity"] = waste_bool.get()
                data["waste"]["graph"] = waste_graph_bool.get()
                data["waste"]["index"] = 3
                data["healthcare"]={}
                data["healthcare"]["sensitivity"] = healthcare_bool.get()
                data["healthcare"]["graph"] = healthcare_graph_bool.get()
                data["healthcare"]["index"] = 3
                path='./'
                filename='check' 
                filePath='./'+path+'/'+filename+'.json'
                f=open(filePath)
                check=json.load(f)
                f.close()
                with open(dirpath + "//" + "report_inputs.txt", 'w') as outfile:
                        json.dump(data, outfile)
                if check["check"] == "True":
                  master_path=os.path.dirname(os.path.abspath('infrastructures_gui.py'))
                  fileLoc = master_path+"\\JobRequest.json"
                  f=open(fileLoc)
                  task5json=json.load(f)
                  fileLoc = master_path+"\\SIRMResults.json"
                  f=open(fileLoc)
                  SIRM=json.load(f)                 
                  Spore=arr.get()
                  spore_count=0
                  Indoor_Spore=""
                  Outdoor_Spore=""
                  Underground_Spore=""
                  Spore_Results=[]
                  Spore_Results=[0 for i in range(len(Spore))]
                  i=0
                  b=0
                  j=1
                  
                  violation=True 
                  for c in Spore:
                      Spore_Results[i]=c
                      i=i+1
                  for z in Spore_Results:
                     if z.isspace():
                       spore_count=spore_count+1
                     else:
                       if spore_count==0:
                         if z.isdigit()==True or z == '.':
                           Indoor_Spore=Indoor_Spore+z
                         else:
                           violation=False
                       elif spore_count==1:
                         if z.isdigit()==True or z == '.':
                           Underground_Spore=Underground_Spore+z
                         else:
                           violation=False
                       elif spore_count==2:
                         if z.isdigit()==True or z == '.':
                           Outdoor_Spore=Outdoor_Spore+z
                         else:
                           violation=False
                  
                  if violation==False:
                    tkMessageBox.showinfo("Helper","Task 5 model did not execute enter a valid spore loading number (int or float)")
                  else:
                  
                    task5json["defineScenario"]["filters"][0]["parameters"][0]["values"]["Indoor"]["value"]=SIRM["data"][6]["value"]##AREA CONTAMINATED
                    task5json["defineScenario"]["filters"][0]["parameters"][0]["values"]["Outdoor"]["value"]=SIRM["data"][7]["value"]
                    #print(task5json["defineScenario"]["filters"][0]["parameters"][0]["values"]["Outdoor"]["value"],task5json["defineScenario"]["filters"][0]["parameters"][0]["values"]["Indoor"]["value"])
                    task5json["defineScenario"]["filters"][0]["parameters"][1]["values"]["Outdoor"]["value"]=Outdoor_Spore##LOADING
                    task5json["defineScenario"]["filters"][0]["parameters"][1]["values"]["Underground"]["value"]=Underground_Spore
                    task5json["defineScenario"]["filters"][0]["parameters"][1]["values"]["Indoor"]["value"]=Indoor_Spore

                    task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Commercial"]["value"]=SIRM["data"][1]["value"]
                    task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Industrial"]["value"]=SIRM["data"][0]["value"]
                    task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Agricultural"]["value"]=SIRM["data"][5]["value"]
                    task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Religious"]["value"]=SIRM["data"][2]["value"]
                    task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Government"]["value"]=SIRM["data"][4]["value"]
                    task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Educational"]["value"]=SIRM["data"][3]["value"]
                    percent=[]
                    percent=[0 for i in range(8)]
                    percent[0]=(task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Residential"]["value"])*100
                    percent[1]=(task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Commercial"]["value"])*100 
                    percent[2]=(task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Industrial"]["value"])*100
                    percent[3]=(task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Agricultural"]["value"])*100
                    percent[4]=(task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Religious"]["value"])*100
                    percent[5]=(task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Government"]["value"])*100
                    percent[6]=(task5json["defineScenario"]["filters"][0]["parameters"][2]["values"]["Educational"]["value"])*100
                    headings=[]
                    headings=[0 for i in range(8)]
                    headings=["Residential","Commercial","Industrial","Agricultural","Religious","Government","Educational"]
                    fig, ax = plt.subplots()
                    fig.set_size_inches(2, 2)
                    colors1 = iter([plt.cm.Pastel1(i) for i in range(20)])
                    newvalues = [x for x in percent if x != 0]
                    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(headings, newvalues)]
                    patches, texts = plt.pie(newvalues, shadow=True, colors=colors1, radius=1.2)
                    sort_legend = True
                    if sort_legend:
                        patches, labels, dummy =  zip(*sorted(zip(patches, labels, newvalues),
                                                              key=lambda headings: headings[2],
                                                              reverse=True))
                    lgd=plt.legend(patches, labels, bbox_to_anchor = (1.05, 0.6),fontsize=8)
                    plt.title('Indoor Contamination by Type')
                    fig=plt.savefig('Indoor_Contamination%.png', bbox_extra_artists=(lgd,), bbox_inches="tight")
                    plt.close(fig)
                    realization=realize.get()
                    if realization.isdigit()==True:
                      task5json["numberRealizations"]=realize.get()
                      with open(master_path+'\\newJobRequest.json', 'w') as myfile:
                            json.dump(task5json,myfile)
                      si = subprocess.STARTUPINFO()
                      si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                      execute=master_path+'\\Battelle.EPA.WideAreaDecon.Launcher.exe'
                    
                      _path=master_path+"\\newJobRequest.json"
                      execute=str('"'+master_path+'\\Battelle.EPA.WideAreaDecon.Launcher.exe"')
                      _path=str('"'+master_path+'\\newJobRequest.json"')
                    
                      cmd=execute+" "+_path
                      subprocess.call(cmd,shell=True,startupinfo=si)
                    else:
                       tkMessageBox.showinfo("Entry for Realizaitons is not a number model will not run please enter a number and try again")
            
                infrastructures_from_file.run_file(optimize, self.orders, self.coeffs, self.k)
                if optimize:
                    print(self.leg)

            def saveScenario():
                data = {}
                n0List = []
                n0List.append(waterVar.get())
                n0List.append(energyVar.get())
                n0List.append(transportVar.get())
                n0List.append(communicationsVar.get())
                n0List.append(governmentVar.get())
                n0List.append(agricultureVar.get())
                n0List.append(emerServVar.get())
                n0List.append(wasteVar.get())
                n0List.append(healthcareVar.get())
                data["n0"] = n0List
                #data["p0"] = var6.get().split(" ")
                data["repair_factors"] = var7.get().split(" ")
                data["nLoss"] = var8.get()
                data["tLoss"] = var9.get()
                data["timeSpan"] = var12.get()
                data["nRun"] = var10.get()
                data["paramTypes"] = var13.get().split(" ")
                data["paramIndexes"] = var14.get().split(" ")
                data["infStoichFactor"] = var15.get()
                data["printProgress"] = var1.get()
                data["averaging"] = var2.get()
                data["intervals"] = var3.get()
                #data["agent"] = var4.get()
                data["seedValue"] = var16.get()
                data["name"] = var17.get()
                data["remediationFactor"] = var18.get().split(" ")
                data["contamination"] = var19.get().split(" ")
                data["backups"] = var21.get().split(" ")
                data["backupPercent"] = var22.get().split(" ")
                data["daysBackup"] = var23.get().split(" ")
                data["depBackup"] = var24.get().split(" ")
                data["negatives"] = var25.get()
                files = [('Text Document', '*.txt'), ('JSON File', '*.json')] 
                filename = asksaveasfile(filetypes = files, defaultextension = files, mode="w")
                if filename is None:
                  return
                json.dump(data, filename)
                filename.close()
                    
            def runLoaded():
                files = [('Text Document', '*.txt'), ('JSON File', '*.json')] 
                filename = askopenfilename(filetypes = files, defaultextension = files)
                if ".txt" in filename or ".json" in filename:
                    n0, repair_factors, nLoss, tLoss, timeSpan, nRun, paramTypes, paramIndexes, printProgress, averaging, \
                    contaminatedListAvailable, infStoichFactor, seedValue, name, remediationFactor, contaminated, backups, \
                    backupPercent, daysBackup, depBackup, negatives = infrastructures_from_file.read_file(filename)
                    json_data = open(filename)
                    data = json.load(json_data)
                    with open(dir_path + "//" + "infrastructures_inputs.txt", 'w') as outfile:
                        json.dump(data, outfile)
                    refresh()
                
            def loadCoeff():
                filename = askopenfilename()
                if ".csv" in filename:
                    self.orders, self.coeffs, self.k = coefficients_from_file.load_file(filename)

            def runReports():
                self.leg = report_GUI.main()

            def runSensitivityGUI():
              newPath = dirpath + "//sensitivity_GUI.exe"
              #copyfile(dirpath+"//infrastructures_inputs.txt", dirpath + "//dist//sensitivity_GUI//infrastructures_inputs.txt")
              command_prompt = "cmd /k " + newPath
              if len(str(newPath).split(' ')) <= 1:
                  newPath = newPath
              else:
                newPath = (f"\"{newPath}\"")
              command_prompt = "start /wait cmd /c " + newPath
              print(command_prompt)
              os.system(command_prompt)
              
            def calcEfficiency(oldVar, increaseVar):
              print(oldVar, increaseVar)
              try:
                result = float(oldVar)/float(increaseVar)
                result = result*100
                tkMessageBox.showinfo("Helper", "The efficiency is %.2f %%" % result)
              except:
                tkMessageBox.showerror("Error", "Please enter a number for each value")
        
            def openHelper(infrastructure):
              if infrastructure == "water":
                tkMessageBox.showinfo("Helper", "Water efficiency can be estimated using the percentage of residents that have potable water, or the water treatment capability")
              elif infrastructure == "energy":
                tkMessageBox.showinfo("Helper", "Energy efficiency can be estimated using the percentage of residents of the area with power")
  
              elif infrastructure == "transport":
                transport_window = tk.Tk()
                tframe = tk.Frame(transport_window)
                tframe.grid(row=4, column=2, sticky="nsew")
                oldVar = tk.StringVar()
                increaseVar = tk.StringVar()
                tk.Label(tframe, text="Original Travel Time", font=("Arial", 10)).grid(row=0, column = 0, sticky=tk.E) 
                transport_old = tk.Entry(tframe, textvariable=oldVar)
                transport_old.grid(row=0, sticky=tk.E, column = 1)
                tk.Label(tframe, text="New Travel Time", font=("Arial", 10)).grid(row=1, column = 0, sticky=tk.E) 
                transport_increase = tk.Entry(tframe, textvariable=increaseVar)
                transport_increase.grid(row=1, sticky=tk.W, column = 1)
                tk.Button(tframe, text="Calculate Transporation Efficiency", font=("Arial", 14), bg='#bcbddc',
                          command=lambda: calcEfficiency(transport_old.get(), transport_increase.get())).grid(row=2, sticky=tk.NSEW, column = 0)
                tk.Button(tframe, text="Quit", command=transport_window.destroy, font=("Arial", 14),bg='#FCB1A0').grid(row=2, sticky=tk.NSEW, column = 1)
                tframe.tkraise()
                transport_window.mainloop()
              elif infrastructure == "communications":
                tkMessageBox.showinfo("Helper", "Communication efficiency can be estimated using the percentage of cell sites that are reported as being down. The FCC website is a good resource for this.")
              elif infrastructure == "government":
                tkMessageBox.showinfo("Helper", "Government building closures are reported in gsa.gov, and the percentage closed can be used to estimate percent efficiency")
              elif infrastructure == "agriculture":
                tkMessageBox.showinfo("Helper", "The best metholodogy for estimating agriculture efficiency is using GIS methods.")
              elif infrastructure == "emerServ":
                tkMessageBox.showinfo("Helper", "The best methodology for estimating emergency services is using GIS methods.")
              elif infrastructure == "waste":
                tkMessageBox.showinfo("Helper", "The best methodology for estimating waste management is through GIS methods.")                
              elif infrastructure == "healthcare":
                #healthcare helper
                tkMessageBox.showinfo("Helper", "Healthcare efficiency can be estimated by using the percentage of available hospital beds, or by the percent increase in waiting time")               

            def loadInits():
                filename = askopenfilename()
                self.orders, self.coeffs, self.k = efficiencies_from_file.load_file(filename)
                
            n0, repair_factors, nLoss, tLoss, timeSpan, nRun, paramTypes, paramIndexes, printProgress, averaging, \
                contaminatedListAvailable, infStoichFactor, seedValue, name, remediationFactor, contaminated, backups, \
                backupPercent, daysBackup, depBackup, negatives = infrastructures_from_file.read_file()
           
##            def newcommand():
##                #tk.Label(self, text="Backup infrastructure efficiency (%): ", bg='#f3f2f1',font=("Arial", 10)).grid(row=9, column = 2, sticky=tk.W)
##                var90 = tk.StringVar()
##                BackupPercent = tk.Entry(self, textvariable=var90)
##                BackupPercent_ttp = CreateToolTip(BackupPercent )
##                BackupPercent.insert(0,var90)
##                BackupPercent.grid(row=16, column = 1, sticky=tk.NSEW)
##                Realization={}
##                Realiztaion["Realization"]=var90.get()
##                filename='Realize' 
##                filePath='./'+path+'/'+filename+'.json'
##                with open(filePath,'w') as fp:
##                  json.dump(Realization,fp)
##                return var90.get()

            def get_text():
                text_file=open("path.txt",'w')
                text_file.write(path.get())
                text_file.close()
        

            def task5():
               path='./'
               filename='check' 
               filePath='./'+path+'/'+filename+'.json'
               var=task__5.get()
               other={}
               if var==1:
                 other["check"]="True"
                 with open(filePath,'w') as fp:
                    json.dump(other,fp)
               else:
                 other["check"]="False"
               with open(filePath,'w') as fp:
                    json.dump(other,fp)
                
            mainframe = tk.Frame.__init__(self,parent)
            label = tk.Label(self, text="Stochastic Infrastructure Remediation Model",bg="snow" ,font=("Calibri Light", 40))
            label.grid(row=0, sticky=tk.NSEW, columnspan=4)

            #tk.Button(self, text='Help', bg='#FCB1A0', command= lambda: showPDF(), font=("Arial", 14)).grid(row=0, column=4, sticky=tk.NSEW)
            #Checkboxes
            extra=ttk.LabelFrame(self,text="Extra Commands")
            extra.place(x=490,y=545)
            if printProgress == "true" or printProgress == "True" or printProgress == "1":
                var1 = tk.IntVar(value=int(bool(printProgress)))
            else:
                var1 = tk.IntVar()
            ttk.Checkbutton(extra,text="Print Progress", variable=var1 ).grid(row=1, sticky=tk.W, column = 0)

            if averaging == "true" or averaging == "True" or averaging == "1":
                var2 = tk.IntVar(value=int(bool(averaging)))
            else:
                var2 = tk.IntVar()
           # ttk.Checkbutton(self, text="Show Run-average", variable=var2 ).grid(row=16, sticky=tk.W, column = 0)
            
            if contaminatedListAvailable == "true" or contaminatedListAvailable == "True" or contaminatedListAvailable == "1":
                var3 = tk.IntVar(value=int(bool(contaminatedListAvailable)))
            else:
                var3 = tk.IntVar()
            ttk.Checkbutton(extra,text="Contaminated Infrastructure List Available", variable=var3).grid(row=1, sticky=tk.W, column = 1)

            #var3 = tk.IntVar(value=int(bool(confIntervals)))
##            if averaging == "true" or averaging == "True" or averaging == "1":
##                var2 = tk.IntVar(value=int(bool(averaging)))
##            else:
##                var2 = tk.IntVar()
##            tk.Checkbutton(self, text="Run-average", variable=var2, font=("Arial", 10)).grid(row=16, sticky=tk.W, column = 0)
##            
##            if confIntervals == "true" or confIntervals == "True" or confIntervals == "1":
##                var3 = tk.IntVar(value=int(bool(confIntervals)))
##            else:
##                var3 = tk.IntVar()
##            tk.Checkbutton(self, text="Confidence Intervals", variable=var3, font=("Arial", 10)).grid(row=17, sticky=tk.W, column = 0)

            if negatives == "true" or negatives == "True" or negatives == "1":
                var25 = tk.IntVar(value=int(bool(negatives)))
            else:
                var25 = tk.IntVar()

    
            task__5=tk.IntVar()
            #print(task__5.get())
            #String Parameters
##            tk.Label(self, text="Agent: ", font=("Arial", 10)).grid(row=1, column = 0, sticky=tk.W)
##            var4 = tk.StringVar()
##            choices = ['anthrax','ebola','monkeypox', 'natural_disaster']
##            var4.set(agent)
##            defaulut_agent = agent
##            Agent = tk.OptionMenu(self, var4, *choices)
##            Agent_ttp = CreateToolTip(Agent, 'Select the agent that the scenario will model')
##            Agent.grid(row=1, column = 1)
##            def change_dropdown(choice, foo, bar):
##                default_agent = choice
##            var4.trace('w', change_dropdown)

            [water0, energy0, transport0, communications0, government0, agriculture0, emerServ0, waste0, healthcare0] = n0

            #String Parameters
##            tk.Label(self, text="Initial infrastructure sector efficiencies (%): ", font=("Arial", 10)).grid(row=2, column = 2, sticky=tk.W)
##            var5 = tk.StringVar()
##            N0 = tk.Entry(self, textvariable=var5)
##            N0.insert(0, n0)
##            N0_ttp = CreateToolTip(N0, 'Enter the efficiency of each infrastructure, each followed by a space. Use the order defined fat the bottom.')
##            N0.grid(row=2, column = 3, sticky=tk.NSEW)
            water_bool = tk.IntVar()
            water_graph_bool = tk.IntVar()
            energy_bool = tk.IntVar()
            energy_graph_bool = tk.IntVar()
            transportation_bool = tk.IntVar()
            transportation_graph_bool = tk.IntVar()
            comm_bool = tk.IntVar()
            comm_graph_bool = tk.IntVar()
            gov_bool = tk.IntVar()
            gov_graph_bool = tk.IntVar()
            emer_bool = tk.IntVar()
            emer_graph_bool = tk.IntVar()
            fa_bool = tk.IntVar()
            fa_graph_bool = tk.IntVar()
            waste_bool = tk.IntVar()
            waste_graph_bool = tk.IntVar()
            healthcare_bool = tk.IntVar()
            healthcare_graph_bool = tk.IntVar()

            file=tk.IntVar()
            count=0
            if(count==0):
              water_bool.set(True)
              water_graph_bool.set(True)
              energy_bool.set(True)
              energy_graph_bool.set(True)
              transportation_bool.set(True)
              transportation_graph_bool.set(True)
              comm_bool.set(True)
              comm_graph_bool.set(True)
              gov_bool.set(True)
              gov_graph_bool.set(True)
              emer_bool.set(True)
              emer_graph_bool.set(True)
              fa_bool.set(True)
              fa_graph_bool.set(True)
              waste_bool.set(True)
              waste_graph_bool.set(True)
              healthcare_bool.set(True)
              healthcare_graph_bool.set(True)
              path='./'
              filename='check' 
              filePath='./'+path+'/'+filename+'.json'
              other={}
              other["check"]="False"
              with open(filePath,'w') as fp:
                    json.dump(other,fp)
              master_path = os.path.dirname(os.path.abspath('final_pdf.py'))
              filePath=master_path+'\\'+'path'+'.json'
              other={}
              other["change"]=0
              with open(filePath,'w') as f:
                  path=json.dump(other,f)
              count=count+1
            initial=ttk.LabelFrame(self,text="Initial Percentages")
            initial.place(x=5,y=60)
            ttk.Label(initial, text="Initial water sector efficiency (%): ").grid(row=2, column = 0, sticky=tk.W)         
            waterVar = tk.StringVar()
            water = ttk.Entry(initial, textvariable=waterVar)
            water.insert(0, n0[0])
            water_ttp = CreateToolTip(water, 'Enter water efficiency.')
            water.grid(row=2, column = 1, sticky=tk.NSEW)
            tk.Button(initial, text="...", command= lambda: openHelper('water')).grid(row=2, column=1, sticky=tk.E)

            ttk.Label(initial, text="Initial energy sector efficiency (%): ").grid(row=3, column = 0, sticky=tk.W)
            energyVar = tk.StringVar()
            energy = ttk.Entry(initial, textvariable=energyVar)
            energy.insert(0, n0[1])
            energy_ttp = CreateToolTip(energy, 'Enter energy efficiency.')
            energy.grid(row=3, column = 1, sticky=tk.NSEW)
            tk.Button(initial, text="...", command= lambda: openHelper('energy')).grid(row=3, column=1, sticky=tk.E)

            ttk.Label(initial, text="Initial transportation sector efficiency (%): ").grid(row=4, column = 0, sticky=tk.W)
            transportVar = tk.StringVar()
            transport = ttk.Entry(initial, textvariable=transportVar)
            transport.insert(0, n0[2])
            transport_ttp = CreateToolTip(transport, 'Enter transport efficiency.')
            transport.grid(row=4, column = 1, sticky=tk.NSEW)
            tk.Button(initial, text="...", command= lambda: openHelper('transport')).grid(row=4, column=1, sticky=tk.E)

            ttk.Label(initial, text="Initial communications sector efficiency (%): ").grid(row=5, column = 0, sticky=tk.W)
            communicationsVar = tk.StringVar()
            communications = ttk.Entry(initial, textvariable=communicationsVar)
            communications.insert(0, n0[3])
            communications_ttp = CreateToolTip(communications, 'Enter communications efficiency.')
            communications.grid(row=5, column = 1, sticky=tk.NSEW)
            tk.Button(initial, text="...", command= lambda: openHelper('communications')).grid(row=5, column=1, sticky=tk.E)

            ttk.Label(initial, text="Initial government sector efficiency (%): ").grid(row=6, column = 0, sticky=tk.W)
            governmentVar = tk.StringVar()
            government = ttk.Entry(initial, textvariable=governmentVar)
            government.insert(0, n0[4])
            government_ttp = CreateToolTip(government, 'Enter government efficiency.')
            government.grid(row=6, column = 1, sticky=tk.NSEW)
            tk.Button(initial, text="...", command= lambda: openHelper('government')).grid(row=6, column=1, sticky=tk.E)

            ttk.Label(initial, text="Initial food and agriculture sector efficiency (%): ").grid(row=7, column = 0, sticky=tk.W)
            agricultureVar = tk.StringVar()
            agriculture = ttk.Entry(initial, textvariable=agricultureVar)
            agriculture.insert(0, n0[5])
            agriculture_ttp = CreateToolTip(agriculture, 'Enter agriculture efficiency.')
            agriculture.grid(row=7, column = 1, sticky=tk.NSEW)
            tk.Button(initial, text="...", command= lambda: openHelper('agriculture')).grid(row=7, column=1, sticky=tk.E)


            ttk.Label(initial, text="Initial emergency services sector efficiency (%): ").grid(row=8, column = 0, sticky=tk.W)
            emerServVar = tk.StringVar()
            emerServ = ttk.Entry(initial, textvariable=emerServVar)
            emerServ.insert(0, n0[6])
            emerServ_ttp = CreateToolTip(emerServ, 'Enter emergency services efficiency.')
            emerServ.grid(row=8, column = 1, sticky=tk.NSEW)
            tk.Button(initial, text="...", command= lambda: openHelper('emerServ')).grid(row=8, column=1, sticky=tk.E)


            ttk.Label(initial, text="Initial waste management sector efficiency (%): ").grid(row=9, column = 0, sticky=tk.W)
            wasteVar = tk.StringVar()
            waste = ttk.Entry(initial, textvariable=wasteVar)
            waste.insert(0, n0[7])
            waste_ttp = CreateToolTip(waste, 'Enter waste management efficiency.')
            waste.grid(row=9, column = 1, sticky=tk.NSEW)
            tk.Button(initial, text="...", command= lambda: openHelper('waste')).grid(row=9, column=1, sticky=tk.E)


            ttk.Label(initial, text="Initial healthcare sector efficiency (%): ").grid(row=10, column = 0, sticky=tk.W)
            healthcareVar = tk.StringVar()
            healthcare = ttk.Entry(initial, textvariable=healthcareVar)
            healthcare.insert(0, n0[8])
            healthcare_ttp = CreateToolTip(healthcare, 'Enter healthcare efficiency.')
            healthcare.grid(row=10, column = 1, sticky=tk.NSEW)
            tk.Button(initial, text="...", command= lambda: openHelper('healthcare')).grid(row=10, column=1, sticky=tk.E)

            ttk.Label(initial,text="Initial contaminated infrastructure (%): ").grid(row=13, column = 0, sticky=tk.W)
            var19 = tk.StringVar()
            C0 = ttk.Entry(initial, textvariable=var19)
            C0.insert(0, contaminated)
            C0_ttp = CreateToolTip(C0, 'Enter the percentage of each infrastructure contaminated, each followed by a space. Use the order defined at the bottom. ')
            C0.grid(row=13, column = 1, sticky=tk.NSEW)

##            tk.Label(self, text="Initial populations: ", font=("Arial", 10)).grid(row=12, column = 0, sticky=tk.W)
##            var6 = tk.StringVar()
##            P0 = tk.Entry(self, textvariable=var6)
##            P0_ttp = CreateToolTip(P0, 'Enter the population in the scenario area, the population sick and... ')
##            P0.insert(0, p0)
##            P0.grid(row=12, column = 1, sticky=tk.NSEW)

            ext=ttk.LabelFrame(self,text="Extra Parameters")
            ext.place(x=530,y=335)
            
            remediation=ttk.LabelFrame(self,text="Remediation Parameters")
            remediation.place(x=10,y=390)
            ttk.Label(remediation,text="Realizations for Wide Area Decon Tool: ").grid(row=14, column=0,sticky=tk.W)
            realize=tk.StringVar()
            wide=ttk.Entry(remediation, textvariable=realize)
            wide.grid(row=14, column=1, sticky=tk.NSEW)
            wide_ttp = CreateToolTip(wide, 'Enter Realizations for wide area decontamination tool')
            wide.insert(0, "1")
            ttk.Label(remediation, text="Repair Factors: ").grid(row=1, column = 0, sticky=tk.W)
            var7 = tk.StringVar()
            Repair_factors = ttk.Entry(remediation, textvariable=var7)
            Repair_factors_ttp = CreateToolTip(Repair_factors, 'Enter the repair factor of each infrastructure, each followed by a space. Use the order defined at the bottom. ')
            Repair_factors.insert(0, repair_factors)
            Repair_factors.grid(row=1, column = 1, sticky=tk.NSEW)

            

            ttk.Label(remediation, text="Remediation Factor (%/day): ").grid(row=12, column = 0, sticky=tk.W)
            var18 = tk.StringVar()
            Remediation_factor = ttk.Entry(remediation, textvariable=var18)
            Remediation_factor_ttp = CreateToolTip(Remediation_factor, 'Enter the % decontaminated per day of each infrastructure, each followed by a space. Use the order defined at the bottom')
            Remediation_factor.insert(0, remediationFactor)
            Remediation_factor.grid(row=12, column = 1, sticky=tk.NSEW)

            ttk.Label(ext, text="Amounts of additional infrastructure outages \n(if applicable, %): ").grid(row=12, column = 2, sticky=tk.W)
            var8 = tk.StringVar()
            NLoss = ttk.Entry(ext, textvariable=var8)
            NLoss_ttp = CreateToolTip(NLoss, 'Enter additional percent outages')
            NLoss.insert(0, nLoss)
            NLoss.grid(row=12, column = 3, sticky=tk.NSEW)

            ttk.Label(ext, text="Time of additional infrastructure outages \n(if applicable, days): ").grid(row=13, column = 2, sticky=tk.W)
            var9 = tk.StringVar()
            TLoss = ttk.Entry(ext, textvariable=var9)
            TLoss_ttp = CreateToolTip(TLoss, 'Enter additional time outage')
            TLoss.insert(0, tLoss)
            TLoss.grid(row=13, column = 3, sticky=tk.NSEW)

##            ttk.Label(remediation, text="Days of Remediation: ").grid(row=11, column = 0, sticky=tk.W)
##            var19 = tk.StringVar()
##            TLoss = ttk.Entry(remediation, textvariable=var19)
##            TLoss_ttp = CreateToolTip(TLoss, 'Enter additional time outage')
##            TLoss.insert(0, tLoss)
##            TLoss.grid(row=11, column = 1, sticky=tk.NSEW)


            model=ttk.LabelFrame(self,text="Model Parameters")
            model.place(x=475,y=60)

          
            report_ttp = CreateToolTip(wide, 'Enter Realizations for wide area decontamination tool')
            arr=tk.StringVar()
            Spore=ttk.Entry(model, textvariable=arr)
            ttk.Label(model,text="Enter Wide Area Decon Spore Loading (Indoor,Underground,Outdoor):  ").grid(row=2, column=2,sticky=tk.W)
            Spore.grid(row=2, column=3,sticky=tk.W)
            Spore_ttp = CreateToolTip(wide, 'Enter Realizations for wide area decontamination tool')
            Spore.insert(0, "2.8 2.6 1.7")


            
            ttk.Label(model, text="Number of stochastic runs:").grid(row=3, column = 2, sticky=tk.W)
            var10 = tk.StringVar()
            NRun = ttk.Entry(model, textvariable=var10)
            NRun_ttp = CreateToolTip(NRun, 'Enter the number of runs')
            NRun.insert(0, nRun)
            NRun.grid(row=3, column = 3, sticky=tk.NSEW)

            ttk.Label(model, text="Simulation Length (days): ").grid(row=4, column = 2, sticky=tk.W)
            var12 = tk.StringVar()
            TimeSpan = ttk.Entry(model, textvariable=var12)
            TimeSpan_ttp = CreateToolTip(TimeSpan, 'Enter the total time of the simulation')
            TimeSpan.insert(0, timeSpan)
            TimeSpan.grid(row=4, column = 3, sticky=tk.NSEW)

            tk.Label(model, text="Parameters to be collected (min, max, average, \nrecover_time(write rt in entry box), final_val): "
                     ).grid(row=5, column = 2, sticky=tk.W)
            var13 = tk.StringVar()
            ParamTypes = ttk.Entry(model, textvariable=var13)
            ParamTypes_ttp = CreateToolTip(ParamTypes, 'Enter the summary statistics you wish to see in a histogram, each followed by a space')
            ParamTypes.insert(0, paramTypes)
            ParamTypes.grid(row=5, column = 3, sticky=tk.NSEW)

            tk.Label(model, text="Infrastructure indexes of collected parameters: ").grid(row=6, column = 2, sticky=tk.W)
            var14 = tk.StringVar()
            ParamIndexes = ttk.Entry(model, textvariable=var14)
            ParamIndexes_ttp = CreateToolTip(ParamIndexes, 'Enter the indexes of the infrastructures you wish to see the above summary statistics for, each followed by a space')
            ParamIndexes.insert(0, paramIndexes)
            ParamIndexes.grid(row=6, column = 3, sticky=tk.NSEW)

            tk.Label(model, text="Infrastructure Stoichiometric Factor: ").grid(row=7, column = 2, sticky=tk.W)
            var15 = tk.StringVar()
            InfStoichFactor = ttk.Entry(model, textvariable=var15)
            InfStoichFactor_ttp = CreateToolTip(InfStoichFactor, 'Enter the overall Infrastructure Stoichiometric Factor ')
            InfStoichFactor.insert(0, infStoichFactor)
            InfStoichFactor.grid(row=7, column = 3, sticky=tk.NSEW)

            ttk.Label(model, text="Seed: ").grid(row=8, column = 2, sticky=tk.W)
            var16 = tk.StringVar()
            SeedValue = ttk.Entry(model, textvariable=var16)
            SeedValue.insert(0, seedValue)
            SeedValue.grid(row=8, column = 3, sticky=tk.NSEW)
            ttk.Label(self, text="").grid(row=1, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=2, sticky=tk.W, column = 0)

            ttk.Label(self, text="").grid(row=3, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=4, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=5, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=6, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=7, sticky=tk.W, column = 1)
            ttk.Label(self, text="").grid(row=8, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=9, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=10, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=11, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=12, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=13, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=14, sticky=tk.W, column = 3)
            ttk.Label(self, text="").grid(row=15, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=16, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=17, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=18, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=19, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=20, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=21, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=22, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=23, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=24, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=25, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=26, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=27, sticky=tk.W, column = 3)
            tk.Label(model, text="Results Chart Name: ").grid(row=9, column = 2, sticky=tk.W)
            var17 = tk.StringVar()
            #tk.Label(model, text="Enter Report output path: ").grid(row=2, column = 2,stick=tk.W)
            ChartName = ttk.Entry(model, textvariable=var17)
            ChartName_ttp = CreateToolTip(ChartName, 'Enter the name of the scenario (no spaces)')
            ChartName.insert(0, name)
            ChartName.grid(row=9, column = 3, sticky=tk.NSEW)
            
       
           
            tk.Label(ext, text="Backup infrastructure indexes of parameters: ").grid(row=8, column = 2, sticky=tk.W)
            var21 = tk.StringVar()
            Backup = ttk.Entry(ext, textvariable=var21)
            Backup_ttp = CreateToolTip(Backup, 'Enter the index of any backup infrastructures, each followed by a space. Keep the same order between the backup inputs. You will need to have individual entries for each dependant infrastructure, even if the same infrastructure is a backup')
            Backup.insert(0, backups)
            Backup.grid(row=8, column = 3, sticky=tk.NSEW)

            ttk.Label(ext, text="Backup infrastructure efficiency (%): ").grid(row=9, column = 2, sticky=tk.W)
            var22 = tk.StringVar()
            BackupPercent = ttk.Entry(ext, textvariable=var22)
            BackupPercent_ttp = CreateToolTip(BackupPercent, 'Enter the percent efficiency of any backup infrastructures, each followed by a space. Keep the same order between the backup inputs. You will need to have individual entries for each dependant infrastructure, even if the same infrastructure is a backup')
            BackupPercent.insert(0, backupPercent)
            BackupPercent.grid(row=9, column = 3, sticky=tk.NSEW)
            ttk.Label(self, text=" ").grid(row=28, sticky=tk.W, column = 2)

            ttk.Label(ext, text="Days backup is available: ").grid(row=10, column = 2, sticky=tk.W)
            var23 = tk.StringVar()
            BackupDays = ttk.Entry(ext, textvariable=var23)
            BackupDays_ttp = CreateToolTip(BackupDays, 'Enter the number of days the backup is available for each dependant infrastructure, each followed by a space. Keep the same order between the backup inputs. You will need to have individual entries for each dependant infrastructure, even if the same infrastructure is a backup')
            BackupDays.insert(0, daysBackup)
            BackupDays.grid(row=10, column = 3)

            tk.Label(ext, text="Dependant infrastructure indexes of parameters: ").grid(row=11, column = 2, sticky=tk.W)
            var24 = tk.StringVar()
            DepBackup = ttk.Entry(ext, textvariable=var24)
            DepBackup_ttp = CreateToolTip(DepBackup, 'Enter the indexes of the infrastructures dependant on the above backups. Keep the same order between the backup inputs')
            DepBackup.insert(0, depBackup)
            DepBackup.grid(row=11, column = 3, sticky=tk.NSEW)
            #Index Note
            note = ttk.Label(self,text="Infrastructure indexes (used in initial infrastructure sector efficiencies, repair factors, " \
                                        "and infrastructure indexes of parameters) are water (0), energy (1), transport services (2), " \
                                        "\ncommunications services (3), government facilities (4), food and agriculture (5), emergency services " \
                                        "(6), waste management (7),  healthcare (8)", #healthcare (9), \nchemical (10), " \
                                        #"commercial facilities (11), manufacturing (12), dams (13), defense (14), and nuclear (15).", \
                                        font=("Arial Bold", 10), borderwidth=2, relief="groove")
            note.grid(row=39, column = 0, columnspan = 6, sticky=tk.NSEW)

            ttk.Checkbutton(extra,text='Reduce Parent Efficiency', var=var25).grid(row=2, sticky=tk.W, column = 1)
            ttk.Checkbutton(extra,text='Add Wide Area Decontamination Results',variable=task__5, command=task5).grid(row=2, sticky=tk.W, column = 0) ###TASK 5 BUTTON
            change=tk.BooleanVar()
            
            tk.Button(self, text='Run GUI Scenario',command= lambda: run(False),font=("Arial", 14), bg='DarkSeaGreen1',
                      ).grid(row=30, column=0,sticky=tk.NSEW, columnspan=2)
            tk.Label(self,text='Change PDF Location:',bg="snow" ).grid(row=27, column=0,sticky=tk.NSEW)
            file_path=tk.StringVar()
            path=ttk.Entry(self,textvariable=file_path)
            path.grid(row=27, column=1, sticky=tk.NSEW)
            master_path = os.path.dirname(os.path.abspath('final_pdf.py'))
            path.insert(0, str(master_path))
           
            def switchFunction():
              master_path = os.path.dirname(os.path.abspath('final_pdf.py'))
              if change.get():
                 var=file_path.get()
                 filename='path' 
                 filePath=master_path+'\\'+filename+'.json'
                 other={}
                 other["path"]=var
                 other["change"]=1
                 with open(filePath,'w') as fp:
                    json.dump(other,fp)
              else:
                 other={}
                 other["change"]=0
                 filename='path' 
                 filePath=master_path+'\\'+filename+'.json'
                 with open(filePath,'w') as fp:
                    json.dump(other,fp) 
            switch = ttk.Checkbutton(self, command=switchFunction,variable=change).grid(row=27,column = 2,sticky=tk.W)
            
            tk.Button(self, text='Save Scenario',font=("Arial", 14), bg='misty rose', command= lambda: saveScenario(),
                      ).grid(row=31, column=0, sticky=tk.NSEW, columnspan=2)
            #tk.Button(self, text='Quit', bg='#C0C0C0', command=self.destroy, font=("Arial", 14)).grid(row=19, column=0, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Load Coefficients', font=("Arial", 14), bg='light cyan',
                      command= lambda: loadCoeff()).grid(row=32, column=0, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Load Scenario', font=("Arial", 14), bg='azure2',
                      command= lambda: runLoaded()).grid(row=33, column=0, sticky=tk.NSEW, columnspan=2)
            #tk.Button(self, text='Select Reports', font=("Arial", 14), bg='#efd566', command= lambda: runReports()).grid(row=18, column=0, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Sensitivity Analysis', font=("Arial", 14),
                      bg='azure', command= lambda: runSensitivityGUI()).grid(row=33, column=2, sticky=tk.NSEW, columnspan=2)

            #GUI Spacing
            for i in range(1,9):
                self.grid_rowconfigure(i, weight=1, uniform="foo")
            for i in range(0,4):
                self.grid_columnconfigure(i, weight=1, uniform="bar")
            Report_Value=ttk.LabelFrame(self,text='Report Value Selection',width=200,height=100)
            Report_Value.place(x=1000, y=55)
        
            ttk.Checkbutton(Report_Value,text='Show Water Sensitivity', var=water_bool,
                           ).grid(row=1, sticky=tk.W, column = 5)
            ttk.Checkbutton(Report_Value,text='Show Water Recovery Histogram', var=water_graph_bool,
                           ).grid(row=2, sticky=tk.W, column = 5)
            

            ttk.Checkbutton(Report_Value,text='Show Energy Sensitivity', var=energy_bool).grid(row=3, sticky=tk.W, column = 5)
            ttk.Checkbutton(Report_Value,text='Show Energy Recovery Histogram', var=energy_graph_bool).grid(row=4, sticky=tk.W, column = 5)

            ttk.Checkbutton(Report_Value,text='Show Transportation Sensitivity', var=transportation_bool).grid(row=5, sticky=tk.W, column = 5)
            ttk.Checkbutton(Report_Value,text='Show Transportation Recovery Histogram', var=transportation_graph_bool).grid(row=6, sticky=tk.W, column = 5)

            ttk.Checkbutton(Report_Value,text='Show Communications Sensitivity', var=comm_bool).grid(row=7, sticky=tk.W, column = 5)
            ttk.Checkbutton(Report_Value,text='Show Communications Recovery Histogram', var=comm_graph_bool).grid(row=8, sticky=tk.W, column = 5)

            ttk.Checkbutton(Report_Value,text='Show Government Sensitivity', var=gov_bool).grid(row=9, sticky=tk.W, column = 5)
            ttk.Checkbutton(Report_Value,text='Show Government Recovery Histogram', var=gov_graph_bool).grid(row=10, sticky=tk.W, column = 5)

            ttk.Checkbutton(Report_Value,text='Show Food/Agriculture Sensitivity', var=fa_bool).grid(row=11, sticky=tk.W, column = 5)
            ttk.Checkbutton(Report_Value,text='Show Food/Agriculture Recovery Histogram', var=fa_graph_bool).grid(row=12, sticky=tk.W, column = 5)

            ttk.Checkbutton(Report_Value, text='Show Emergency Services Sensitivity', var=emer_bool).grid(row=13, sticky=tk.W, column = 5)
            ttk.Checkbutton(Report_Value, text='Show Emergency Services Recovery Histogram', var=emer_graph_bool).grid(row=14, sticky=tk.W, column = 5)

            ttk.Checkbutton(Report_Value, text='Show Waste Management Sensitivity', var=waste_bool ).grid(row=15, sticky=tk.W, column = 5)
            ttk.Checkbutton(Report_Value, text='Show Waste Management Recovery Histogram', var=waste_graph_bool ).grid(row=16, sticky=tk.W, column = 5)

            ttk.Checkbutton(Report_Value,text='Show Healthcare Sensitivity', var=healthcare_bool ).grid(row=17, sticky=tk.W, column = 5)
            ttk.Checkbutton(Report_Value,text='Show Healthcare Recovery Histogram', var=healthcare_graph_bool).grid(row=18, sticky=tk.W, column = 5)
            Button(Report_Value, text = 'Select All',font=("sans" ,10,), command = select_all).grid(row=31, sticky=tk.N, column  =5 )
            Button(Report_Value, text = 'Deselect All',font=("sans",10), command = deselect_all).grid(row=32, sticky=tk.N, column = 5)
            ttk.Label(self, text="                                                                                                             ").grid(row=78, sticky=tk.W, column = 5)
            #print(self.orders, self.coeffs, self.k)
            #tk.Button(self, text='Save Report Values', bg='#FCB1A0', command= lambda: saveValues(), font=("Arial", 14)).grid(row=18, column=5, sticky=tk.NSEW)
            #tk.Button(self, text='Cancel', bg='#C0C0C0', command=self.destroy, font=("Arial", 14)).grid(row=18, column=6, sticky=tk.NSEW)
    global app
    app = TKinterWindow()
    app.title("Stochastic Infrastructure Remediation Model")
    app.configure(background = 'alice blue')
    app.protocol("WM_DELETE_WINDOW", app.appClose)
    done = False
    while not done:
      app.mainloop()

if __name__ == '__main__':

    def refresh():
        app.destroy()
        leg = main()

    leg = main()



