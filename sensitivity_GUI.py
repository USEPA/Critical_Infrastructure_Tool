# -*- coding: utf-8 -*-
"""
"""

#import statements
import sys
import numpy as np
if (sys.version_info > (3, 0)):
  import tkinter as tk
  from tkinter import ttk
  from tkinter import *
else:
  import Tkinter as tk
  from Tkinter import ttl
import infrastructures_from_file
import coefficients_from_file
import tkinter.messagebox as tkMessageBox
import json
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from shutil import copyfile
from fpdf import FPDF
import PyPDF2
from PIL import Image
import os
#import geopandas
if (sys.version_info > (3,0)):
  from tkinter.filedialog import askopenfilename
  from tkinter.filedialog import asksaveasfile
else:
  from tkFileDialog import askopenfilename
  from tkFileDialog import asksaveasfile 

from plotnine import *
import shutil



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
        filename = fileLoc
        copyfile(filename, temp_file)
        json_data = open(filename)
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
            data["name"] = self.parameter + "_" + str(name).split(".")[0] + " " + str(self.sector)
            with open(fileLoc, "w") as outfile:
              json.dump(data, outfile)
            self.leg = infrastructures_from_file.run_file(False, orders, coeffs, k)
            result = pd.read_csv(dir_path + "\\Results\\" + data["name"] + ".csv")
            for i in range(len(result["Sectors"])):
              new_row = pd.DataFrame({'Sector': result["Sectors"][i], 'RT': result["Recovery Times"][i], 'Value': start}, index=[0])
              results = pd.concat([results,new_row])
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
        
        p = ggplot(results, aes(x='Value', y='RT', color = 'Sector')) + xlab(self.parameter) + ylab("Recovery Time (days)") + geom_point() + geom_line()
        file_name = self.parameter + "_" + self.sector
        
        path_name = dir_path + "\\Sensitivity\\"


        p.save(filename=file_name, path = path_name, verbose = False, device= "jpeg")
        copyfile(temp_file, fileLoc)
        width= 60
        height = 10
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Times', 'B', 16)
        pdf.cell(width, height,"Sensitivity Analysis for "+self.sector+" on "+ self.parameter)
        pdf.ln(" ")
        pdf.set_font('Times', 'B', 14)
        pdf.cell(width,height,"Introduction")
        pdf.ln(" ")
        pdf.set_font('Times', '', 12)
        text_1="A sensitivity analysis was conducted on a selected value from the Stochastic Infrastructure Remediation Model "
        text_2="(SIRM). The SIRM allows for a series of interconnected infrastructure sectors to be modeled and considers the "
        text_3="realistic variability of the impact of a CBRN (chemical, biological, radiological, and nuclear) event."
        text_4="Sensitivity Analysis will determine how "+self.parameter + " is affected  by recovery time. The closer the slope"
        text_5="to zero the less of an impact it will have in the model."
        pdf.cell(width,height,text_1,ln=1)
        pdf.cell(width,height,text_2,ln=1)
        pdf.cell(width,height,text_3,ln=1)
        pdf.cell(width,height,text_4,ln=1)
        pdf.cell(width,height,text_5,ln=1)
        pdf.set_font('Times','B',14)
        pdf.cell(width, height, "Sensitivity Graph",ln=1)
        pdf.set_font('Times', 'B', 12)
        graph_name = path_name + file_name + ".png"
        pdf.cell(width, height,"     "+ ggt)
        pdf.ln(" ")
        pdf.image(graph_name, w = 200)
        pdf.set_font('Times', 'B', 12)
        text = "Slope"
        if self.parameter == "Days Backup":
           text= "Reduction (days) in recovery time for an increase in 1 day backup"
        if self.parameter == "Efficiency of Backups":
          text = "Reduction (days) in recovery time for an increase in 1% backup efficiency"
        if self.parameter == "Initial Efficiency":
          text = "Reduction (days) in recovery time for an increase in 1% initial efficiency"
        if self.parameter == "Repair Factors":
          text = "Reduction (days) in recovery time for an increase in 0.1 repair factor"
        pdf.ln(" ")
        pdf.ln(" ")
        pdf.ln(" ")
        pdf.ln(" ")
        pdf.ln(" ")
        pdf.ln(" ")
        pdf.ln(" ")
        pdf.ln(" ")
        pdf.set_font('Times', 'B', 14)
        pdf.cell(width, height,text)
        pdf.ln(" ")
        pdf.set_font('Times', '', 12)
        pdf.cell(width, height,"Below is the sector and "+text+" for the",ln=1)
        pdf.cell(width, height, "parameter breakdown for the sensitivity analysis.",ln=1)
        pdf.ln(" ")
        pdf.set_font('Times', 'B', 12)
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
        filePath=dir_path+'\\'+'DATA'+'.json'
        with open(filePath) as f:
            path=json.load(f)
        if path['change']==1:
          path_name = path['path']+"\\Sensitivity\\"
        CHECK_FOLDER = os.path.isdir(path_name)
        if not CHECK_FOLDER:
          os.makedirs(path_name)
        pdf.output(path_name + file_name + "_Report.pdf", 'F')
                
def main():
    LARGE_FONT= ("Verdana", 24)

    class TKinterWindow(tk.Tk):

        def __init__(self, *args, **kwargs):

            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)
            style=ttk.Style(self)
            self.tk.call('source','azure.tcl')
            style.theme_use('azure')

            container.pack(side="top", fill="both", expand = True)

            container.grid_rowconfigure(20, weight=1)
            container.grid_columnconfigure(4, weight=1)

            self.frames = {}

            frame = StartPage(container, self)
            frame.configure(bg="snow")

            self.frames[StartPage] = frame

            frame.grid(row=1, column=1, sticky="nsew")

            #self.geometry("700x500")
            

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
            mainframe = tk.Frame.__init__(self,parent)
            dirpath = os.getcwd()
            
                
            self.leg = None
            def hide_rf(checkbox):
              if checkbox == 1:
                  rp_min_text.grid()
                  rp_min.grid()
                  rp_max_text.grid()
                  rp_max.grid()
                  rp_steps_text.grid()
                  rp_steps.grid()
              else:
                  rp_min_text.grid_remove()
                  rp_min.grid_remove()
                  rp_max_text.grid_remove()
                  rp_max.grid_remove()
                  rp_steps_text.grid_remove()
                  rp_steps.grid_remove()

            def hide_bd(checkbox):
              if checkbox == 1:
                  bd_min_text.grid()
                  bd_min.grid()
                  bd_max_text.grid()
                  bd_max.grid()
                  bd_steps_text.grid()
                  bd_steps.grid()
              else:
                  rp_min_text.grid_remove()
                  rp_min.grid_remove()
                  rp_max_text.grid_remove()
                  rp_max.grid_remove()
                  rp_steps_text.grid_remove()
                  rp_steps.grid_remove()

            def hide_be(checkbox):
              if checkbox == 1:
                  be_min_text.grid()
                  be_min.grid()
                  be_max_text.grid()
                  be_max.grid()
                  be_steps_text.grid()
                  be_steps.grid()
              else:
                  be_min_text.grid_remove()
                  be_min.grid_remove()
                  be_max_text.grid_remove()
                  be_max.grid_remove()
                  be_steps_text.grid_remove()
                  be_steps.grid_remove()

            def hide_ie(checkbox):
              if checkbox == 1:
                  ie_min_text.grid()
                  ie_min.grid()
                  ie_max_text.grid()
                  ie_max.grid()
                  ie_steps_text.grid()
                  ie_steps.grid()
              else:
                  ie_min_text.grid_remove()
                  ie_min.grid_remove()
                  ie_max_text.grid_remove()
                  ie_max.grid_remove()
                  ie_steps_text.grid_remove()
                  ie_steps.grid_remove()

            def run():
              rf = self.rf_bool.get()
              dir_path = os.path.dirname(os.path.realpath(__file__))
              path_name = dir_path + "\\Sensitivity\\"
              if os.path.isdir(path_name):
                shutil.rmtree(path_name)
              os.mkdir(path_name)
              
              backup_days  = self.backup_days_bool.get()
              backup_efficiency = self.backup_efficiency_bool.get()
              initial_efficiency = self.initial_efficiency_bool.get()
              sectors = sector_list
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
            bool_list = [self.water_bool, self.energy_bool, self.transportation_bool, self.comm_bool,
                         self.gov_bool, self.emer_bool, self.fa_bool, self.waste_bool, self.healthcare_bool]
            sector_list = ["Water", "Energy", "Transportation", "Communications", "Government", "Emergency Services",
                           "Food and Agriculture", "Waste Management", "Healthcare"]
            label = tk.Label(self, text="                     Sensitivity Analysis Tool", bg="snow",font=("Calibri Light", 30))
            label.grid(row=0, sticky=tk.NSEW,columnspan=4)
            #string definitions
            rf_range_min = tk.StringVar()
            inf_stoich_range_min = tk.StringVar()
            backup_days_range_min = tk.StringVar()
            backup_efficiency_range_min = tk.StringVar()
            initial_efficiency_range_min = tk.StringVar()

            rf_range_max = tk.StringVar()
            inf_stoich_range_max = tk.StringVar()
            backup_days_range_max = tk.StringVar()
            backup_efficiency_range_max = tk.StringVar()
            initial_efficiency_range_max = tk.StringVar()

            rf_steps = tk.StringVar()
            backup_days_steps = tk.StringVar()
            backup_efficiency_steps = tk.StringVar()
            initial_efficiency_steps = tk.StringVar()
            analyze=ttk.LabelFrame(self,text='Parameters to Analyze')
            analyze.place(x=0,y=60)

            #ttk.Label(remediation, text='Parameters to Analyze').grid(row=1, sticky=tk.W, column = 0)
            rf_check = ttk.Checkbutton(analyze, text='Repair Factors', var=self.rf_bool).grid(row=2, sticky=tk.W, column = 0)
            db_check = ttk.Checkbutton(analyze, text='Days Backup', var=self.backup_days_bool).grid(row=4, sticky=tk.W, column = 0)
            de_check = ttk.Checkbutton(analyze, text='Efficiency of Backup', var=self.backup_efficiency_bool).grid(row=6, sticky=tk.W, column = 0)
            ie_check = ttk.Checkbutton(analyze, text='Initial Efficiency', var=self.initial_efficiency_bool).grid(row=8, sticky=tk.W, column = 0)
            analyze_min=ttk.LabelFrame(self,text='Parameter Mins')
            analyze_min.place(x=160,y=60)

            #tk.Label(self, text='Parameter Mins', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 1)
            rp_min_text = ttk.Label(analyze_min, text='Repair Factors Min:', font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 1)
            bd_min_text = ttk.Label(analyze_min, text='Days Backup Min:', font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 1)
            be_min_text = ttk.Label(analyze_min, text='Efficiency of Backup Min:', font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 1)
            ie_min_text = ttk.Label(analyze_min, text='Initial Efficiency Min:', font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 1)

            rp_min = ttk.Entry(analyze_min, textvariable=rf_range_min, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 1)
            bd_min = ttk.Entry(analyze_min, textvariable=backup_days_range_min, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 1)
            be_min = ttk.Entry(analyze_min, textvariable=backup_efficiency_range_min, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 1)
            ie_min = ttk.Entry(analyze_min, textvariable=initial_efficiency_range_min, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 1)

            
            analyze_max=ttk.LabelFrame(self,text='Parameters Maxes')
            analyze_max.place(x=330,y=60)
            #ttk.Label(analyze_max, text='Parameter Maxes', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 2)
            rp_max_text = ttk.Label(analyze_max, text='Repair Factors Max:', font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 2)
            bd_max_text = ttk.Label(analyze_max, text='Days Backup Max:', font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 2)
            be_max_text = ttk.Label(analyze_max, text='Efficiency of Backup Max:', font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 2)
            ie_max_text = ttk.Label(analyze_max, text='Initial Efficiency Max:', font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 2)

            rp_max = ttk.Entry(analyze_max, textvariable=rf_range_max, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 2)
            bd_max = ttk.Entry(analyze_max, textvariable=backup_days_range_max, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 2)
            be_max = ttk.Entry(analyze_max, textvariable=backup_efficiency_range_max, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 2)
            ie_max = ttk.Entry(analyze_max, textvariable=initial_efficiency_range_max, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 2)
            analyze_param=ttk.LabelFrame(self,text='Parameters Steps')
            analyze_param.place(x=500,y=60)

            #ttk.Label(analyze_param, text='Parameter Steps', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 3)
            rp_steps_text = ttk.Label(analyze_param, text='Repair Factors Steps:', font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 3)
            bd_steps_text = ttk.Label(analyze_param, text='Days Backup Steps:', font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 3)
            be_steps_text = ttk.Label(analyze_param, text='Efficiency of Backup Steps:', font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 3)
            ie_steps_text = ttk.Label(analyze_param, text='Initial Efficiency Steps:', font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 3)

            rp_steps = ttk.Entry(analyze_param, textvariable=rf_steps, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 3)
            bd_steps = ttk.Entry(analyze_param, textvariable=backup_days_steps, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 3)
            be_steps = ttk.Entry(analyze_param, textvariable=backup_efficiency_steps, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 3)
            ie_steps = ttk.Entry(analyze_param, textvariable=initial_efficiency_steps, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 3)
            ttk.Label(self, text="").grid(row=1, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=2, sticky=tk.W, column = 0)

            ttk.Label(self, text="").grid(row=3, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=4, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=5, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=6, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=7, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=8, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=9, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=10, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=11, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=12, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=13, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=14, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=15, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=16, sticky=tk.W, column = 0)
            ttk.Label(self, text="").grid(row=17, sticky=tk.W, column = 0)
          
            
           

            tk.Label(self, text='                                                                                 ',bg="snow" ,font=("Arial", 12)).grid(row=16, sticky=tk.W, column = 10)
            Infra=ttk.LabelFrame(self,text='Infrastructure Sectors to Analyze:')
            Infra.place(x=670,y=60)
            for i in range(len(sector_list)):
              ttk.Checkbutton(Infra, text=sector_list[i], var=bool_list[i]).grid(row=2+i, sticky=tk.W, column = 4)
            #print(self.orders, self.coeffs, self.k)
            tk.Button(self, text='Run Analysis', bg='#C7FCA0', command= lambda: run(), font=("Arial", 14)).grid(row=16, column=2, sticky=tk.NSEW,columnspan=2)
            #tk.Button(self, text='Cancel', bg='#C0C0C0', command=self.destroy, font=("Arial", 14)).grid(row=18, column=4, sticky=tk.NSEW)
        
    global app
    app = TKinterWindow()
    app.title("Report")
    #app.protocol("WM_DELETE_WINDOW", app.appClose)
    app.mainloop()
    


if __name__ == '__main__':

    def refresh():
        app.destroy()
        leg = main()
    leg = main()



