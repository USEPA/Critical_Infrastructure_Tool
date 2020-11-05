# -*- coding: utf-8 -*-
"""
"""

#import statements
import sys
import numpy as np
if (sys.version_info > (3, 0)):
  import tkinter as tk
else:
  import Tkinter as tk
import infrastructures_from_file
import coefficients_from_file
import tkinter.messagebox as tkMessageBox
import json
import seaborn as sns
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
      return mpl.colors.to_hex((1-mix)*c1 + mix*c2)
    
    def hex_to_rgb(self, value):
      value = value.lstrip('#')
      lv = len(value)
      return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def runAnalysis(self, sectors):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fileLoc = dir_path + "//" + "infrastructures_inputs.txt"
        temp_file = dir_path + "//" + "infrastructures_inputs_temp.txt"
        copyfile(fileLoc, temp_file)
        json_data = open(fileLoc)
        data = json.load(json_data)
        start = self.min
        step = (self.max-self.min)/self.steps
        orders, coeffs, k = coefficients_from_file.load_file(dir_path + "//"+ "default.csv")
        results = pd.DataFrame()
        sectorInt = sectors.index(self.sector)
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
                
def main():
    LARGE_FONT= ("Verdana", 24)

    class TKinterWindow(tk.Tk):

        def __init__(self, *args, **kwargs):

            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)

            container.pack(side="top", fill="both", expand = True)

            container.grid_rowconfigure(20, weight=1)
            container.grid_columnconfigure(4, weight=1)

            self.frames = {}

            frame = StartPage(container, self)

            self.frames[StartPage] = frame

            frame.grid(row=1, column=1, sticky="nsew")

            #self.geometry("700x500")
            

            self.show_frame(StartPage)

        def show_frame(self, cont):
            
            frame = self.frames[cont]
            #frame.config(bg="#F7FCF6")
            frame.tkraise()
            
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
              rf = rf_bool.get()
              backup_days  = backup_days_bool.get()
              backup_efficiency = backup_efficiency_bool.get()
              initial_efficiency = initial_efficiency_bool.get()
              sectors = sector_list
              water = water_bool.get()
              energy = energy_bool.get()
              transportation = transportation_bool.get()
              comm = comm_bool.get()
              gov = gov_bool.get()
              emer = emer_bool.get()
              fa = fa_bool.get()
              waste = waste_bool.get()
              healthcare = healthcare_bool.get()
              bools = [water, energy, transportation, comm, gov, emer, fa, waste, healthcare]
              new_sector_list = []
              for i in range(len(bools)):
                if (bools[i])>0:
                  new_sector_list.append(sectors[i])
              if rf>0:
                for sector in new_sector_list:
                  individual_run = sensitivityAnalysis("Repair Factors", rf_range_min.get(),
                                            rf_range_max.get(), rf_steps.get(), sector)
                  individual_run.runAnalysis(sectors)
                  
              if backup_days>0:
                for sector in new_sector_list:
                  individual_run = sensitivityAnalysis("Days Backup", backup_days_range_min.get(),
                                            backup_days_range_max.get(), backup_days_steps.get(), sector)
                  individual_run.runAnalysis(sectors)
                  
              if backup_efficiency>0:
                for sector in new_sector_list:
                  individual_run = sensitivityAnalysis("Efficiency of Backups", backup_efficiency_range_min.get(),
                                            backup_efficiency_range_max.get(), backup_efficiency_steps.get(), sector)
                  individual_run.runAnalysis(sectors)
                  
              if initial_efficiency>0:
                for sector in new_sector_list:
                  individual_run = sensitivityAnalysis("Initial Efficiency", initial_efficiency_range_min.get(),
                                            initial_efficiency_range_max.get(), initial_efficiency_steps.get(), sector)
                  individual_run.runAnalysis(sectors)
            
            #bool definitions
            rf_bool = tk.IntVar()
            backup_days_bool = tk.IntVar()
            backup_efficiency_bool = tk.IntVar()
            initial_efficiency_bool = tk.IntVar()
            
            water_bool = tk.IntVar()
            energy_bool = tk.IntVar()
            transportation_bool = tk.IntVar()
            comm_bool = tk.IntVar()
            gov_bool = tk.IntVar()
            emer_bool = tk.IntVar()
            fa_bool = tk.IntVar()
            waste_bool = tk.IntVar()
            healthcare_bool = tk.IntVar()
            bool_list = [water_bool, energy_bool, transportation_bool, comm_bool,
                         gov_bool, emer_bool, fa_bool, waste_bool, healthcare_bool]
            sector_list = ["Water", "Energy", "Transportation", "Communications", "Government", "Emergency Services",
                           "Food and Agriculture", "Waste Management", "Healthcare"]
            
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

            tk.Label(self, text='Parameters to Analyze', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 0)
            rf_check = tk.Checkbutton(self, text='Repair Factors', var=rf_bool, font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 0)
            db_check = tk.Checkbutton(self, text='Days Backup', var=backup_days_bool, font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 0)
            de_check = tk.Checkbutton(self, text='Efficiency of Backup', var=backup_efficiency_bool, font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 0)
            ie_check = tk.Checkbutton(self, text='Initial Efficiency', var=initial_efficiency_bool, font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 0)

            tk.Label(self, text='Parameter Mins', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 1)
            rp_min_text = tk.Label(self, text='Repair Factors Min:', font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 1)
            bd_min_text = tk.Label(self, text='Days Backup Min:', font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 1)
            be_min_text = tk.Label(self, text='Efficiency of Backup Min:', font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 1)
            ie_min_text = tk.Label(self, text='Initial Efficiency Min:', font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 1)

            rp_min = tk.Entry(self, textvariable=rf_range_min, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 1)
            bd_min = tk.Entry(self, textvariable=backup_days_range_min, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 1)
            be_min = tk.Entry(self, textvariable=backup_efficiency_range_min, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 1)
            ie_min = tk.Entry(self, textvariable=initial_efficiency_range_min, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 1)

            tk.Label(self, text='Parameter Maxes', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 2)
            rp_max_text = tk.Label(self, text='Repair Factors Max:', font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 2)
            bd_max_text = tk.Label(self, text='Days Backup Max:', font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 2)
            be_max_text = tk.Label(self, text='Efficiency of Backup Max:', font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 2)
            ie_max_text = tk.Label(self, text='Initial Efficiency Max:', font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 2)

            rp_max = tk.Entry(self, textvariable=rf_range_max, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 2)
            bd_max = tk.Entry(self, textvariable=backup_days_range_max, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 2)
            be_max = tk.Entry(self, textvariable=backup_efficiency_range_max, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 2)
            ie_max = tk.Entry(self, textvariable=initial_efficiency_range_max, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 2)

            tk.Label(self, text='Parameter Steps', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 3)
            rp_steps_text = tk.Label(self, text='Repair Factors Steps:', font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 3)
            bd_steps_text = tk.Label(self, text='Days Backup Steps:', font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 3)
            be_steps_text = tk.Label(self, text='Efficiency of Backup Steps:', font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 3)
            ie_steps_text = tk.Label(self, text='Initial Efficiency Steps:', font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 3)

            rp_steps = tk.Entry(self, textvariable=rf_steps, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 3)
            bd_steps = tk.Entry(self, textvariable=backup_days_steps, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 3)
            be_steps = tk.Entry(self, textvariable=backup_efficiency_steps, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 3)
            ie_steps = tk.Entry(self, textvariable=initial_efficiency_steps, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 3)

            tk.Label(self, text='Infrastructure Sectors to Analyze:', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 4)
            for i in range(len(sector_list)):
              tk.Checkbutton(self, text=sector_list[i], var=bool_list[i], font=("Arial", 10)).grid(row=2+i, sticky=tk.W, column = 4)
            #print(self.orders, self.coeffs, self.k)
            tk.Button(self, text='Run Analysis', bg='#C7FCA0', command= lambda: run(), font=("Arial", 14)).grid(row=18, column=3, sticky=tk.NSEW)
            tk.Button(self, text='Cancel', bg='#C0C0C0', command=self.destroy, font=("Arial", 14)).grid(row=18, column=4, sticky=tk.NSEW)

    global app
    app = TKinterWindow()
    app.title("Report")
    app.mainloop()

if __name__ == '__main__':

    def refresh():
        app.destroy()
        leg = main()
    leg = main()



