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
else:
  import Tkinter as tk
import infrastructures_from_file
import coefficients_from_file
import report_GUI
#import sensitivity_GUI
import tkinter.messagebox as tkMessageBox
#from fiona import _shim, schema
#import infrastructures_mapping
import json
from inspect import getsourcefile
from os.path import abspath


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
        self.wraplength = 180   #pixels
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
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class sensitivityAnalysis(object):
    def __init__(self, parameter, minval, maxval, steps, sector):
        self.parameter = parameter
        self.min = float(minval)
        self.max = float(maxval)
        self.steps = int(steps)
        self.sector = sector

    def colorFader(self, c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
      c1=np.array(mpl.colors.to_rgb(c1))
      c2=np.array(mpl.colors.to_rgb(c2))
      print((1-mix)*c1 + mix*c2)
      return mpl.colors.to_hex(abs((1-mix)*c1 + mix*c2))
    
    def hex_to_rgb(self, value):
      value = value.lstrip('#')
      lv = len(value)
      return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def runAnalysis(self, sectors):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fileLoc = dir_path + "//" + "infrastructures_inputs.txt"
        temp_file = dir_path + "//" + "infrastructures_inputs_temp.txt"
        files = [('Text Document', '*.txt'), ('JSON File', '*.json')] 
        #filename = askopenfilename(filetypes = files, defaultextension = files)
        copyfile(fileLoc, temp_file)
        json_data = open(fileLoc)
        data = json.load(json_data)
        start = self.min
        step = (self.max-self.min)/self.steps
        orders, coeffs, k = coefficients_from_file.load_file(dir_path + "//"+ "default.csv")
        results = pd.DataFrame()
        sectorInt = sectors.index(self.sector)
        if (self.min > self.max):
            tkMessageBox.showerror("Error","Minimum values must be less than maximum values")
            raise ValueError("Minimum values must be less than maximum values")

        for i in range(self.steps):
            depBackups = list(range(9))
            depBackups.pop(sectorInt)
            backs = [sectorInt] * (len(sectors)-1)
            if self.parameter == "Repair Factors":
              data["repair_factors"][sectorInt] = start
            elif self.parameter == "Initial Efficiency":
              data["n0"][sectorInt] = start
            elif self.parameter == "Days Backup":
              days = [start]*(len(sectors)-1)
              percents = [90] * (len(sectors)-1)
              data["daysBackup"] = days
              data["backupPercent"] = percents
              data["depBackup"] = depBackups
              data["backups"] = backs
            elif self.parameter == "Efficiency of Backups":
              days = [10] * (len(sectors)-1)
              percents = [start]*(len(sectors)-1)
              data["daysBackup"] = days
              data["backupPercent"] = percents
              data["depBackup"] = depBackups
              data["backups"] = backs
            name = start
            if start < 1:
              name = round(start * 100, 0)
            data["name"] = self.parameter + "_" + str(name).split(".")[0]
            with open(fileLoc, "w") as outfile:
              json.dump(data, outfile)
            self.leg = infrastructures_from_file.run_file(False, orders, coeffs, k)
            result = pd.read_csv(dir_path + "\\Results\\" + data["name"] + ".csv")
            for i in range(len(result["Sectors"])):
              new_row = {'Sector': result["Sectors"][i], 'RT': result["Recovery Times"][i], 'Value': start}
              results = results.append(new_row, ignore_index=True)
            start += step
        plt.style.use('ggplot')
        ggt = self.sector + " " + self.parameter + " vs Sector Recovery Times"
        slope_results = pd.DataFrame()
        newSectors = list(set(results['Sector']))
        for i in range(len(newSectors)):
          sectorResults = results[results.Sector.eq(newSectors[i])]
          m, b = np.polyfit(sectorResults['Value'], sectorResults['RT'], 1)
          new_row = {'Sector': newSectors[i], 'Slope': m, 'Intercept': b}
          slope_results = slope_results.append(new_row, ignore_index=True)
        print(slope_results)     
        p = ggplot(results, aes(x='Value', y='RT', color = 'Sector')) + xlab(self.parameter) + ylab("Recovery Time (days)") + geom_point() + geom_line() + ggtitle(ggt)
        file_name = self.parameter + "_" + self.sector
        path_name = dir_path + "\\Sensitivity\\"
        p.save(filename=file_name, path = path_name, verbose = False)
        copyfile(temp_file, fileLoc)
        width= 60
        height = 10
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Times', 'B', 12)
        graph_name = path_name + file_name + ".png"
        pdf.image(graph_name)
        text = "Slope"
        if self.parameter == "Days Backup":
          text = "Reduction (days) in recovery time for an increase in 1 day backup"
        if self.parameter == "Efficiency of Backups":
          text = "Reduction (days) in recovery time for an increase in 1% backup efficiency"
        if self.parameter == "Initial Efficiency":
          text = "Reduction (days) in recovery time for an increase in 1% initial efficiency"
        if self.parameter == "Repair Factors":
          text = "Reduction (days) in recovery time for an increase in 0.1 repair factor"
          
        data = ["Infrastructure Sector",text ]
        white = np.array([255, 255, 255])
        pdf.cell(width, height, str(data[0]), border=1)
        pdf.cell(135, height, str(data[1]), border=1, ln=1)
        n = 9
        c1='white' 
        c2='green' 
        slope_max= max(abs(slope_results["Slope"]))
        #pdf.cell(width, height, str(data[2]), border=1, ln=1)
        for i in range(len(slope_results["Slope"])):
          slope = abs(round(float(slope_results["Slope"][i]), 2))
          if self.parameter == "Repair Factors":
            slope_max= max(abs(slope_results["Slope"]))/10
            slope = round(abs(float(slope_results["Slope"][i])), 2)/10
          color= self.colorFader(c1,c2,slope/slope_max)
          new_color = self.hex_to_rgb(color)
          (x1, x2, x3) = new_color
          pdf.set_fill_color(x1, x2, x3)
          pdf.cell(width, height, str(slope_results["Sector"][i]), border=1)
          pdf.cell(135, height, str(round(slope,2)), border=1, ln=1, fill=True, align = 'C')
          #pdf.cell(width, height,text, border=1, ln=1)

        pdf.output(path_name + file_name + "_Report.pdf", 'F')

class sensitivity_GUI():
  def __init__(self):
    sensitivity_frame = tk.Tk()

    sensitivity_frame.grid_rowconfigure(20, weight=1)
    sensitivity_frame.grid_columnconfigure(4, weight=1)

    def runSensitivity():
      rf = self.rf_bool.get()
              
      backup_days  = self.backup_days_bool.get()
      backup_efficiency = self.backup_efficiency_bool.get()
      initial_efficiency = self.initial_efficiency_bool.get()
      sectors = self.sector_list
      water = self.water_bool.get()
      energy = self.energy_bool.get()
      transportation = self.transportation_bool.get()
      comm = self.comm_bool.get()
      gov = self.gov_bool.get()
      emer = self.emer_bool.get()
      fa = self.fa_bool.get()
      waste = self.waste_bool.get()
      healthcare = self.healthcare_bool.get()
      bools = [water, energy, transportation, comm, gov, emer, fa, waste, healthcare]
      new_sector_list = []
      print(rf, backup_days, backup_efficiency, initial_efficiency)
      print(bools)
      for i in range(len(bools)):
        if (bools[i])>0:
          new_sector_list.append(sectors[i])
        if rf>0:
          if ((float(rf_range_min.get()) <= 0) or (float(rf_range_max.get()) <= 0) or (float(rf_range_min.get()) >= 1) or (float(rf_range_max.get()) >= 1)):
            tkMessageBox.showerror("Error","Repair factor values must be between 0 and 1")
            raise ValueError("Repair factor values must be between 0 and 1")
          try:
            (float(rf_steps.get()))
          except:
            tkMessageBox.showerror("Error","Steps value must be integer")
            raise ValueError("Steps value must be integer")
          for sector in new_sector_list:
            individual_run = sensitivityAnalysis("Repair Factors", rf_range_min.get(),
                                            rf_range_max.get(), rf_steps.get(), sector)
            individual_run.runAnalysis(sectors)
                  
        if backup_days>0:
          try:
            (float(backup_days_steps.get()))
          except:
            tkMessageBox.showerror("Error","Steps value must be integer")
            raise ValueError("Steps value must be integer")
          for sector in new_sector_list:
            individual_run = sensitivityAnalysis("Days Backup", backup_days_range_min.get(),
                                            backup_days_range_max.get(), backup_days_steps.get(), sector)
            individual_run.runAnalysis(sectors)
                  
          if backup_efficiency>0:
            try:
              (float(backup_efficiency_steps.get()))
            except:
              tkMessageBox.showerror("Error","Steps value must be integer")
              raise ValueError("Steps value must be integer")
            for sector in new_sector_list:
              individual_run = sensitivityAnalysis("Efficiency of Backups", backup_efficiency_range_min.get(),
                                            backup_efficiency_range_max.get(), backup_efficiency_steps.get(), sector)
              individual_run.runAnalysis(sectors)
                  
          if initial_efficiency>0:
            try:
              (float(initial_efficiency_steps.get()))
            except:
              tkMessageBox.showerror("Error","Steps value must be integer")
              raise ValueError("Steps value must be integer")
            for sector in new_sector_list:
              individual_run = sensitivityAnalysis("Initial Efficiency", initial_efficiency_range_min.get(),
                                            initial_efficiency_range_max.get(), initial_efficiency_steps.get(), sector)
              individual_run.runAnalysis(sectors)
            
            #bool definitions
    self.rf_bool = tk.BooleanVar()
    self.backup_days_bool = tk.BooleanVar()
 
    self.backup_efficiency_bool = tk.BooleanVar()
    self.initial_efficiency_bool = tk.BooleanVar()
            
    self.water_bool = tk.BooleanVar()
    self.energy_bool = tk.BooleanVar()
    self.transportation_bool = tk.BooleanVar()
    self.comm_bool = tk.BooleanVar()
    self.gov_bool = tk.BooleanVar()
    self.emer_bool = tk.BooleanVar()
    self.fa_bool = tk.BooleanVar()
    self.waste_bool = tk.BooleanVar()
    self.healthcare_bool = tk.BooleanVar()
    self.bool_list = [self.water_bool, self.energy_bool, self.transportation_bool, self.comm_bool,
                         self.gov_bool, self.emer_bool, self.fa_bool, self.waste_bool, self.healthcare_bool]
    self.sector_list = ["Water", "Energy", "Transportation", "Communications", "Government", "Emergency Services",
                           "Food and Agriculture", "Waste Management", "Healthcare"]
            
            #string definitions
    self.rf_range_min = tk.StringVar()
    self.inf_stoich_range_min = tk.StringVar()
    self.backup_days_range_min = tk.StringVar()
    self.backup_efficiency_range_min = tk.StringVar()
    self.initial_efficiency_range_min = tk.StringVar()

    self.rf_range_max = tk.StringVar()
    self.inf_stoich_range_max = tk.StringVar()
    self.backup_days_range_max = tk.StringVar()
    self.backup_efficiency_range_max = tk.StringVar()
    self.initial_efficiency_range_max = tk.StringVar()

    self.rf_steps = tk.StringVar()
    self.backup_days_steps = tk.StringVar()
    self.backup_efficiency_steps = tk.StringVar()
    self.initial_efficiency_steps = tk.StringVar()

    tk.Label(sensitivity_frame, text='Parameters to Analyze', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 0)
    rf_check = tk.Checkbutton(sensitivity_frame, text='Repair Factors', var=self.rf_bool, font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 0)
    db_check = tk.Checkbutton(sensitivity_frame, text='Days Backup', var=self.backup_days_bool, font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 0)
    de_check = tk.Checkbutton(sensitivity_frame, text='Efficiency of Backup', var=self.backup_efficiency_bool, font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 0)
    ie_check = tk.Checkbutton(sensitivity_frame, text='Initial Efficiency', var=self.initial_efficiency_bool, font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 0)

    tk.Label(sensitivity_frame, text='Parameter Mins', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 1)
    rp_min_text = tk.Label(sensitivity_frame, text='Repair Factors Min:', font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 1)
    bd_min_text = tk.Label(sensitivity_frame, text='Days Backup Min:', font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 1)
    be_min_text = tk.Label(sensitivity_frame, text='Efficiency of Backup Min:', font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 1)
    ie_min_text = tk.Label(sensitivity_frame, text='Initial Efficiency Min:', font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 1)

    rp_min = tk.Entry(sensitivity_frame, textvariable=self.rf_range_min, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 1)
    bd_min = tk.Entry(sensitivity_frame, textvariable=self.backup_days_range_min, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 1)
    be_min = tk.Entry(sensitivity_frame, textvariable=self.backup_efficiency_range_min, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 1)
    ie_min = tk.Entry(sensitivity_frame, textvariable=self.initial_efficiency_range_min, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 1)

    tk.Label(sensitivity_frame, text='Parameter Maxes', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 2)
    rp_max_text = tk.Label(sensitivity_frame, text='Repair Factors Max:', font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 2)
    bd_max_text = tk.Label(sensitivity_frame, text='Days Backup Max:', font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 2)
    be_max_text = tk.Label(sensitivity_frame, text='Efficiency of Backup Max:', font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 2)
    ie_max_text = tk.Label(sensitivity_frame, text='Initial Efficiency Max:', font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 2)

    rp_max = tk.Entry(sensitivity_frame, textvariable=self.rf_range_max, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 2)
    bd_max = tk.Entry(sensitivity_frame, textvariable=self.backup_days_range_max, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 2)
    be_max = tk.Entry(sensitivity_frame, textvariable=self.backup_efficiency_range_max, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 2)
    ie_max = tk.Entry(sensitivity_frame, textvariable=self.initial_efficiency_range_max, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 2)

    tk.Label(sensitivity_frame, text='Parameter Steps', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 3)
    rp_steps_text = tk.Label(sensitivity_frame, text='Repair Factors Steps:', font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 3)
    bd_steps_text = tk.Label(sensitivity_frame, text='Days Backup Steps:', font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 3)
    be_steps_text = tk.Label(sensitivity_frame, text='Efficiency of Backup Steps:', font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 3)
    ie_steps_text = tk.Label(sensitivity_frame, text='Initial Efficiency Steps:', font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 3)

    rp_steps = tk.Entry(sensitivity_frame, textvariable=self.rf_steps, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 3)
    bd_steps = tk.Entry(sensitivity_frame, textvariable=self.backup_days_steps, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 3)
    be_steps = tk.Entry(sensitivity_frame, textvariable=self.backup_efficiency_steps, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 3)
    ie_steps = tk.Entry(sensitivity_frame, textvariable=self.initial_efficiency_steps, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 3)

    tk.Label(sensitivity_frame, text='Infrastructure Sectors to Analyze:', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 4)
    for i in range(len(self.sector_list)):
      tk.Checkbutton(sensitivity_frame, text=self.sector_list[i], var=self.bool_list[i], font=("Arial", 10)).grid(row=2+i, sticky=tk.W, column = 4)
      #print(self.orders, self.coeffs, self.k)
    tk.Button(sensitivity_frame, text='Run Analysis', bg='#C7FCA0', command= lambda: runSensitivity(), font=("Arial", 14)).grid(row=18, column=3, sticky=tk.NSEW)
    tk.Button(sensitivity_frame, text='Cancel', bg='#C0C0C0', command=sensitivity_frame.destroy, font=("Arial", 14)).grid(row=18, column=4, sticky=tk.NSEW)

def main():
    LARGE_FONT= ("Verdana", 24)

    class TKinterWindow(tk.Tk):

        def __init__(self, *args, **kwargs):

            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)

            container.pack(side="top", fill="both", expand = True)

            container.grid_rowconfigure(20, weight=1)
            container.grid_columnconfigure(7, weight=1,minsize="600")

            self.frames = {}

            frame = StartPage(container, self)

            self.frames[StartPage] = frame

            frame.grid(row=1, column=1, sticky="nsew")

            self.geometry("1200x750")
            

            self.show_frame(StartPage)

        def show_frame(self, cont):
            
            frame = self.frames[cont]
            #frame.config(bg="#F7FCF6")
            frame.tkraise()
            
    class StartPage(tk.Frame):

        def __init__(self, parent, controller):

            self.leg = None
            #dir_path = os.path.dirname(os.path.realpath(__file__))
            dir_path = os.path.dirname(abspath(getsourcefile(lambda:0)))
            dirpath = os.getcwd()

            self.orders, self.coeffs, self.k = coefficients_from_file.load_file(dir_path + "//"+ "default.csv")
            #print(self.orders, self.coeffs, self.k)

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

                with open(dirpath + "//" + "report_inputs.txt", 'w') as outfile:
                        json.dump(data, outfile)
                self.leg = infrastructures_from_file.run_file(optimize, self.orders, self.coeffs, self.k)
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
                self.leg = sensitivity_GUI()

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
            

            mainframe = tk.Frame.__init__(self,parent)
            label = tk.Label(self, text="Stochastic Infrastructure Remediation Model", font=("Arial", 40))
            label.grid(row=0, sticky=tk.NSEW, columnspan=4)

            #tk.Button(self, text='Help', bg='#FCB1A0', command= lambda: showPDF(), font=("Arial", 14)).grid(row=0, column=4, sticky=tk.NSEW)
            #Checkboxes
            if printProgress == "true" or printProgress == "True" or printProgress == "1":
                var1 = tk.IntVar(value=int(bool(printProgress)))
            else:
                var1 = tk.IntVar()
            tk.Checkbutton(self, text="Print Progress", variable=var1, font=("Arial", 10)).grid(row=15, sticky=tk.W, column = 0)

            if averaging == "true" or averaging == "True" or averaging == "1":
                var2 = tk.IntVar(value=int(bool(averaging)))
            else:
                var2 = tk.IntVar()
            tk.Checkbutton(self, text="Show Run-average", variable=var2, font=("Arial", 10)).grid(row=16, sticky=tk.W, column = 0)
            
            if contaminatedListAvailable == "true" or contaminatedListAvailable == "True" or contaminatedListAvailable == "1":
                var3 = tk.IntVar(value=int(bool(contaminatedListAvailable)))
            else:
                var3 = tk.IntVar()
            tk.Checkbutton(self, text="Contaminated Infrastructure List Available", variable=var3, font=("Arial", 10)).grid(row=17, sticky=tk.W, column = 0)

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
##            N0_ttp = CreateToolTip(N0, 'Enter the efficiency of each infrastructure, each followed by a space. Use the order defined at the bottom.')
##            N0.grid(row=2, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Initial water sector efficiency (%): ", font=("Arial", 10)).grid(row=2, column = 0, sticky=tk.W)         
            waterVar = tk.StringVar()
            water = tk.Entry(self, textvariable=waterVar)
            water.insert(0, n0[0])
            water_ttp = CreateToolTip(water, 'Enter water efficiency.')
            water.grid(row=2, column = 1, sticky=tk.NSEW)
            tk.Button(self, text="...", command= lambda: openHelper('water')).grid(row=2, column=1, sticky=tk.E)

            tk.Label(self, text="Initial energy sector efficiency (%): ", font=("Arial", 10)).grid(row=3, column = 0, sticky=tk.W)
            energyVar = tk.StringVar()
            energy = tk.Entry(self, textvariable=energyVar)
            energy.insert(0, n0[1])
            energy_ttp = CreateToolTip(energy, 'Enter energy efficiency.')
            energy.grid(row=3, column = 1, sticky=tk.NSEW)
            tk.Button(self, text="...", command= lambda: openHelper('energy')).grid(row=3, column=1, sticky=tk.E)

            tk.Label(self, text="Initial transportation sector efficiency (%): ", font=("Arial", 10)).grid(row=4, column = 0, sticky=tk.W)
            transportVar = tk.StringVar()
            transport = tk.Entry(self, textvariable=transportVar)
            transport.insert(0, n0[2])
            transport_ttp = CreateToolTip(transport, 'Enter transport efficiency.')
            transport.grid(row=4, column = 1, sticky=tk.NSEW)
            tk.Button(self, text="...", command= lambda: openHelper('transport')).grid(row=4, column=1, sticky=tk.E)

            tk.Label(self, text="Initial communications sector efficiency (%): ", font=("Arial", 10)).grid(row=5, column = 0, sticky=tk.W)
            communicationsVar = tk.StringVar()
            communications = tk.Entry(self, textvariable=communicationsVar)
            communications.insert(0, n0[3])
            communications_ttp = CreateToolTip(communications, 'Enter communications efficiency.')
            communications.grid(row=5, column = 1, sticky=tk.NSEW)
            tk.Button(self, text="...", command= lambda: openHelper('communications')).grid(row=5, column=1, sticky=tk.E)

            tk.Label(self, text="Initial government sector efficiency (%): ", font=("Arial", 10)).grid(row=6, column = 0, sticky=tk.W)
            governmentVar = tk.StringVar()
            government = tk.Entry(self, textvariable=governmentVar)
            government.insert(0, n0[4])
            government_ttp = CreateToolTip(government, 'Enter government efficiency.')
            government.grid(row=6, column = 1, sticky=tk.NSEW)
            tk.Button(self, text="...", command= lambda: openHelper('government')).grid(row=6, column=1, sticky=tk.E)

            tk.Label(self, text="Initial food and agriculture sector efficiency (%): ", font=("Arial", 10)).grid(row=7, column = 0, sticky=tk.W)
            agricultureVar = tk.StringVar()
            agriculture = tk.Entry(self, textvariable=agricultureVar)
            agriculture.insert(0, n0[5])
            agriculture_ttp = CreateToolTip(agriculture, 'Enter agriculture efficiency.')
            agriculture.grid(row=7, column = 1, sticky=tk.NSEW)
            tk.Button(self, text="...", command= lambda: openHelper('agriculture')).grid(row=7, column=1, sticky=tk.E)


            tk.Label(self, text="Initial emergency services sector efficiency (%): ", font=("Arial", 10)).grid(row=8, column = 0, sticky=tk.W)
            emerServVar = tk.StringVar()
            emerServ = tk.Entry(self, textvariable=emerServVar)
            emerServ.insert(0, n0[6])
            emerServ_ttp = CreateToolTip(emerServ, 'Enter emergency services efficiency.')
            emerServ.grid(row=8, column = 1, sticky=tk.NSEW)
            tk.Button(self, text="...", command= lambda: openHelper('emerServ')).grid(row=8, column=1, sticky=tk.E)


            tk.Label(self, text="Initial waste management sector efficiency (%): ", font=("Arial", 10)).grid(row=9, column = 0, sticky=tk.W)
            wasteVar = tk.StringVar()
            waste = tk.Entry(self, textvariable=wasteVar)
            waste.insert(0, n0[7])
            waste_ttp = CreateToolTip(waste, 'Enter waste management efficiency.')
            waste.grid(row=9, column = 1, sticky=tk.NSEW)
            tk.Button(self, text="...", command= lambda: openHelper('waste')).grid(row=9, column=1, sticky=tk.E)


            tk.Label(self, text="Initial healthcare sector efficiency (%): ", font=("Arial", 10)).grid(row=10, column = 0, sticky=tk.W)
            healthcareVar = tk.StringVar()
            healthcare = tk.Entry(self, textvariable=healthcareVar)
            healthcare.insert(0, n0[8])
            healthcare_ttp = CreateToolTip(healthcare, 'Enter healthcare efficiency.')
            healthcare.grid(row=10, column = 1, sticky=tk.NSEW)
            tk.Button(self, text="...", command= lambda: openHelper('healthcare')).grid(row=10, column=1, sticky=tk.E)

            tk.Label(self, text="Initial contaminated infrastructure (%): ", font=("Arial", 10)).grid(row=13, column = 0, sticky=tk.W)
            var19 = tk.StringVar()
            C0 = tk.Entry(self, textvariable=var19)
            C0.insert(0, contaminated)
            C0_ttp = CreateToolTip(C0, 'Enter the percentage of each infrastructure contaminated, each followed by a space. Use the order defined at the bottom. ')
            C0.grid(row=13, column = 1, sticky=tk.NSEW)

##            tk.Label(self, text="Initial populations: ", font=("Arial", 10)).grid(row=12, column = 0, sticky=tk.W)
##            var6 = tk.StringVar()
##            P0 = tk.Entry(self, textvariable=var6)
##            P0_ttp = CreateToolTip(P0, 'Enter the population in the scenario area, the population sick and... ')
##            P0.insert(0, p0)
##            P0.grid(row=12, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Repair Factors: ", font=("Arial", 10)).grid(row=1, column = 0, sticky=tk.W)
            var7 = tk.StringVar()
            Repair_factors = tk.Entry(self, textvariable=var7)
            Repair_factors_ttp = CreateToolTip(Repair_factors, 'Enter the repair factor of each infrastructure, each followed by a space. Use the order defined at the bottom. ')
            Repair_factors.insert(0, repair_factors)
            Repair_factors.grid(row=1, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Remediation Factor (%/day): ", font=("Arial", 10)).grid(row=12, column = 0, sticky=tk.W)
            var18 = tk.StringVar()
            Remediation_factor = tk.Entry(self, textvariable=var18)
            Remediation_factor_ttp = CreateToolTip(Remediation_factor, 'Enter the % decontaminated per day of each infrastructure, each followed by a space. Use the order defined at the bottom')
            Remediation_factor.insert(0, remediationFactor)
            Remediation_factor.grid(row=12, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Amounts of additional infrastructure outages \n(if applicable, %): ", font=("Arial", 10)).grid(row=12, column = 2, sticky=tk.W)
            var8 = tk.StringVar()
            NLoss = tk.Entry(self, textvariable=var8)
            NLoss_ttp = CreateToolTip(NLoss, 'Enter additional percent outages')
            NLoss.insert(0, nLoss)
            NLoss.grid(row=12, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Time of additional infrastructure outages \n(if applicable, days): ", font=("Arial", 10)).grid(row=13, column = 2, sticky=tk.W)
            var9 = tk.StringVar()
            TLoss = tk.Entry(self, textvariable=var9)
            TLoss_ttp = CreateToolTip(TLoss, 'Enter additional time outage')
            TLoss.insert(0, tLoss)
            TLoss.grid(row=13, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Days of Remediation: ", font=("Arial", 10)).grid(row=11, column = 0, sticky=tk.W)
            var9 = tk.StringVar()
            TLoss = tk.Entry(self, textvariable=var9)
            TLoss_ttp = CreateToolTip(TLoss, 'Enter additional time outage')
            TLoss.insert(0, tLoss)
            TLoss.grid(row=11, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Number of stochastic runs:", font=("Arial", 10)).grid(row=2, column = 2, sticky=tk.W)
            var10 = tk.StringVar()
            NRun = tk.Entry(self, textvariable=var10)
            NRun_ttp = CreateToolTip(NRun, 'Enter the number of runs')
            NRun.insert(0, nRun)
            NRun.grid(row=2, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Simulation Length (days): ", font=("Arial", 10)).grid(row=3, column = 2, sticky=tk.W)
            var12 = tk.StringVar()
            TimeSpan = tk.Entry(self, textvariable=var12)
            TimeSpan_ttp = CreateToolTip(TimeSpan, 'Enter the total time of the simulation')
            TimeSpan.insert(0, timeSpan)
            TimeSpan.grid(row=3, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Parameters to be collected (min, max, average, \nrecover_time(write rt in entry box), final_val): ",
                     font=("Arial", 10)).grid(row=4, column = 2, sticky=tk.W)
            var13 = tk.StringVar()
            ParamTypes = tk.Entry(self, textvariable=var13)
            ParamTypes_ttp = CreateToolTip(ParamTypes, 'Enter the summary statistics you wish to see in a histogram, each followed by a space')
            ParamTypes.insert(0, paramTypes)
            ParamTypes.grid(row=4, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Infrastructure indexes of collected parameters: ", font=("Arial", 10)).grid(row=5, column = 2, sticky=tk.W)
            var14 = tk.StringVar()
            ParamIndexes = tk.Entry(self, textvariable=var14)
            ParamIndexes_ttp = CreateToolTip(ParamIndexes, 'Enter the indexes of the infrastructures you wish to see the above summary statistics for, each followed by a space')
            ParamIndexes.insert(0, paramIndexes)
            ParamIndexes.grid(row=5, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Infrastructure Stoichiometric Factor: ", font=("Arial", 10)).grid(row=6, column = 2, sticky=tk.W)
            var15 = tk.StringVar()
            InfStoichFactor = tk.Entry(self, textvariable=var15)
            InfStoichFactor_ttp = CreateToolTip(InfStoichFactor, 'Enter the overall Infrastructure Stoichiometric Factor ')
            InfStoichFactor.insert(0, infStoichFactor)
            InfStoichFactor.grid(row=6, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Seed: ", font=("Arial", 10)).grid(row=7, column = 2, sticky=tk.W)
            var16 = tk.StringVar()
            SeedValue = tk.Entry(self, textvariable=var16)
            SeedValue.insert(0, seedValue)
            SeedValue.grid(row=7, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Results Chart Name: ", font=("Arial", 10)).grid(row=1, column = 2, sticky=tk.W)
            var17 = tk.StringVar()
            ChartName = tk.Entry(self, textvariable=var17)
            ChartName_ttp = CreateToolTip(ChartName, 'Enter the name of the scenario (no spaces)')
            ChartName.insert(0, name)
            ChartName.grid(row=1, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Backup infrastructure indexes of parameters: ", font=("Arial", 10)).grid(row=8, column = 2, sticky=tk.W)
            var21 = tk.StringVar()
            Backup = tk.Entry(self, textvariable=var21)
            Backup_ttp = CreateToolTip(Backup, 'Enter the index of any backup infrastructures, each followed by a space. Keep the same order between the backup inputs. You will need to have individual entries for each dependant infrastructure, even if the same infrastructure is a backup')
            Backup.insert(0, backups)
            Backup.grid(row=8, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Backup infrastructure efficiency (%): ", font=("Arial", 10)).grid(row=9, column = 2, sticky=tk.W)
            var22 = tk.StringVar()
            BackupPercent = tk.Entry(self, textvariable=var22)
            BackupPercent_ttp = CreateToolTip(BackupPercent, 'Enter the percent efficiency of any backup infrastructures, each followed by a space. Keep the same order between the backup inputs. You will need to have individual entries for each dependant infrastructure, even if the same infrastructure is a backup')
            BackupPercent.insert(0, backupPercent)
            BackupPercent.grid(row=9, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Days backup is available: ", font=("Arial", 10)).grid(row=10, column = 2, sticky=tk.W)
            var23 = tk.StringVar()
            BackupDays = tk.Entry(self, textvariable=var23)
            BackupDays_ttp = CreateToolTip(BackupDays, 'Enter the number of days the backup is available for each dependant infrastructure, each followed by a space. Keep the same order between the backup inputs. You will need to have individual entries for each dependant infrastructure, even if the same infrastructure is a backup')
            BackupDays.insert(0, daysBackup)
            BackupDays.grid(row=10, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Dependant infrastructure indexes of parameters: ", font=("Arial", 10)).grid(row=11, column = 2, sticky=tk.W)
            var24 = tk.StringVar()
            DepBackup = tk.Entry(self, textvariable=var24)
            DepBackup_ttp = CreateToolTip(DepBackup, 'Enter the indexes of the infrastructures dependant on the above backups. Keep the same order between the backup inputs')
            DepBackup.insert(0, depBackup)
            DepBackup.grid(row=11, column = 3, sticky=tk.NSEW)
            
            #Index Note
            note = tk.Label(self, text="Infrastructure indexes (used in initial infrastructure sector efficiencies, repair factors, " \
                                        "and infrastructure indexes of parameters) are water (0), energy (1), transport services (2), " \
                                        "\ncommunications services (3), government facilities (4), food and agriculture (5), emergency services " \
                                        "(6), waste management (7),  healthcare (8)", #healthcare (9), \nchemical (10), " \
                                        #"commercial facilities (11), manufacturing (12), dams (13), defense (14), and nuclear (15).", \
                                        font=("Arial Bold", 10), bg='#F9F8E5', borderwidth=2, relief="groove")
            note.grid(row=20, column = 0, columnspan = 4, sticky=tk.NSEW)

            #Buttons


            tk.Checkbutton(self, text='Reduce Parent Efficiency', var=var25, font=("Arial", 10)).grid(row=16, sticky=tk.W, column = 0)

            tk.Button(self, text='Run GUI Scenario',bg='#C7FCA0',command= lambda: run(False), font=("Arial", 14)).grid(row=15, column=2, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Save Scenario', bg='#FCB1A0', command= lambda: saveScenario(), font=("Arial", 14)).grid(row=18, column=2, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Quit', bg='#C0C0C0', command=self.destroy, font=("Arial", 14)).grid(row=19, column=2, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Load Coefficients', font=("Arial", 14), bg='#A0D4FC', command= lambda: loadCoeff()).grid(row=17, column=2, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Load Scenario', font=("Arial", 14), bg='#bcbddc', command= lambda: runLoaded()).grid(row=16, column=2, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Select Reports', font=("Arial", 14), bg='#efd566', command= lambda: runReports()).grid(row=18, column=0, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Sensitivity Analysis', font=("Arial", 14), bg='#61ccc7', command= lambda: runSensitivityGUI()).grid(row=19, column=0, sticky=tk.NSEW, columnspan=2)

            #GUI Spacing
            for i in range(1,9):
                self.grid_rowconfigure(i, weight=1, uniform="foo")
            for i in range(0,4):
                self.grid_columnconfigure(i, weight=1, uniform="bar")

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

            tk.Label(self, text='Report Value Selection', font=("Arial", 12)).grid(row=0, sticky=tk.W, column = 5)
            tk.Checkbutton(self, text='Show Water Sensitivity', var=water_bool, font=("Arial", 10)).grid(row=1, sticky=tk.W, column = 5)
            tk.Checkbutton(self, text='Show Water Recovery Histogram', var=water_graph_bool, font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 5)

            tk.Checkbutton(self, text='Show Energy Sensitivity', var=energy_bool, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 5)
            tk.Checkbutton(self, text='Show Energy Recovery Histogram', var=energy_graph_bool, font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 5)

            tk.Checkbutton(self, text='Show Transportation Sensitivity', var=transportation_bool, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 5)
            tk.Checkbutton(self, text='Show Transportation Recovery Histogram', var=transportation_graph_bool, font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 5)

            tk.Checkbutton(self, text='Show Communications Sensitivity', var=comm_bool, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 5)
            tk.Checkbutton(self, text='Show Communications Recovery Histogram', var=comm_graph_bool, font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 5)

            tk.Checkbutton(self, text='Show Government Sensitivity', var=gov_bool, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 5)
            tk.Checkbutton(self, text='Show Government Recovery Histogram', var=gov_graph_bool, font=("Arial", 10)).grid(row=10, sticky=tk.W, column = 5)

            tk.Checkbutton(self, text='Show Food/Agriculture Sensitivity', var=fa_bool, font=("Arial", 10)).grid(row=11, sticky=tk.W, column = 5)
            tk.Checkbutton(self, text='Show Food/Agriculture Recovery Histogram', var=fa_graph_bool, font=("Arial", 10)).grid(row=12, sticky=tk.W, column = 5)

            tk.Checkbutton(self, text='Show Emergency Services Sensitivity', var=emer_bool, font=("Arial", 10)).grid(row=13, sticky=tk.W, column = 5)
            tk.Checkbutton(self, text='Show Emergency Services Recovery Histogram', var=emer_graph_bool, font=("Arial", 10)).grid(row=14, sticky=tk.W, column = 5)

            tk.Checkbutton(self, text='Show Waste Management Sensitivity', var=waste_bool, font=("Arial", 10)).grid(row=15, sticky=tk.W, column = 5)
            tk.Checkbutton(self, text='Show Waste Management Recovery Histogram', var=waste_graph_bool, font=("Arial", 10)).grid(row=16, sticky=tk.W, column = 5)

            tk.Checkbutton(self, text='Show Healthcare Sensitivity', var=healthcare_bool, font=("Arial", 10)).grid(row=17, sticky=tk.W, column = 5)
            tk.Checkbutton(self, text='Show Healthcare Recovery Histogram', var=healthcare_graph_bool, font=("Arial", 10)).grid(row=18, sticky=tk.W, column = 5)            
            #print(self.orders, self.coeffs, self.k)

            #tk.Button(self, text='Save Report Values', bg='#FCB1A0', command= lambda: saveValues(), font=("Arial", 14)).grid(row=18, column=5, sticky=tk.NSEW)
            #tk.Button(self, text='Cancel', bg='#C0C0C0', command=self.destroy, font=("Arial", 14)).grid(row=18, column=6, sticky=tk.NSEW)
 

    global app
    app = TKinterWindow()
    app.title("Stochastic Infrastructure Remediation Model")
    app.mainloop()

if __name__ == '__main__':

    def refresh():
        app.destroy()
        leg = main()
    leg = main()



