# -*- coding: utf-8 -*-
"""
report_gui.py
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
import tkinter.messagebox as tkMessageBox
import json


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
    def __init__(self, inf_name, parameter, value, minval, maxval, steps):
        self.inf_name = inf_name
        self.parameter = parameter
        self.min = minval
        self.max = maxval
        self.steps = steps

    def runAnalysis(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        json_data = open(fname)
        data = json.load(json_data)
        start = self.min
        step = (self.max-self.min)/steps
        orders, coeffs, k = coefficients_from_file.load_file(dir_path + "//"+ "default.csv")
        import os
        os.rmdir("InterimSensitivity")
        while (start < self.max):
            data[self.parameter] = start
            name = start
            if start < 1:
              name = round(start * 10, 0)
            data["name"] = self.parameter + "_" + name
            json.dump(data)
            self.leg = infrastructures_from_file.run_file(False, orders, coeffs, k)
            #run_infrastructure
            #write to excel file
            start += step

    def compileResults(self):
        

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
            
            #bool definitions
            rf_bool = tk.IntVar()
            inf_stoich = tk.IntVar()
            backup_days = tk.IntVar()
            backup_efficiency = tk.IntVar()
            initial_efficiency = tk.IntVar()
            
            water_bool = tk.IntVar()
            water_bool = tk.IntVar()
            energy_bool = tk.IntVar()
            transportation_bool = tk.IntVar()
            comm_bool = tk.IntVar()
            gov_bool = tk.IntVar
            emer_bool = tk.IntVar()
            fa_bool = tk.IntVar()
            waste_bool = tk.IntVar()
            healthcare_bool = tk.IntVar()

            #string definitions
            rf_range = tk.StringVar()
            inf_stoich_range = tk.StringVar()
            backup_days_range = tk.StringVar()
            backup_efficiency_range = tk.StringVar()
            initial_efficiency_range = tk.StringVar()

            rf_steps = tk.StringVar()
            inf_stoich_steps = tk.StringVar()
            backup_days_steps = tk.StringVar()
            backup_efficiency_steps = tk.StringVar()
            initial_efficiency_steps = tk.StringVar()

            tk.Label(self, text='Parameters to Analyze', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Repair Factors', var=rf_bool, font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Infrastructure Stoichiometric Factor', var=inf_stoich, font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Days Backup', var=backup_days, font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Efficiency of Backup', var=backup_efficiency, font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Initial Efficiency', var=initial_efficiency, font=("Arial", 10)).grid(row=10, sticky=tk.W, column = 0)

            tk.Label(self, text='Parameter Ranges', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 1)
            tk.Label(self, text='Repair Factors Range:', font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 1)
            tk.Label(self, text='Infrastructure Stoichiometric Factor Range:', font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 1)
            tk.Label(self, text='Days Backup Range:', font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 1)
            tk.Label(self, text='Efficiency of Backup Range:', font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 1)
            tk.Label(self, text='Initial Efficiency Range:', font=("Arial", 10)).grid(row=10, sticky=tk.W, column = 1)

            tk.Entry(self, textvariable=rf_range, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 1)
            tk.Entry(self, textvariable=inf_stoich_range, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 1)
            tk.Entry(self, textvariable=backup_days_range, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 1)
            tk.Entry(self, textvariable=backup_efficiency_range, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 1)
            tk.Entry(self, textvariable=initial_efficiency_range, font=("Arial", 10)).grid(row=11, sticky=tk.W, column = 1)

            tk.Label(self, text='Parameter Steps', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 3)
            tk.Label(self, text='Repair Factors Steps:', font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 3)
            tk.Label(self, text='Infrastructure Stoichiometric Factor Steps:', font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 3)
            tk.Label(self, text='Days Backup Steps:', font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 3)
            tk.Label(self, text='Efficiency of Backup Steps:', font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 3)
            tk.Label(self, text='Initial Efficiency Steps:', font=("Arial", 10)).grid(row=10, sticky=tk.W, column = 3)

            tk.Entry(self, textvariable=rf_steps, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 3)
            tk.Entry(self, textvariable=inf_stoich_steps, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 3)
            tk.Entry(self, textvariable=backup_days_steps, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 3)
            tk.Entry(self, textvariable=backup_efficiency_steps, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 3)
            tk.Entry(self, textvariable=initial_efficiency_steps, font=("Arial", 10)).grid(row=11, sticky=tk.W, column = 3)

            tk.Label(self, text='Infrastructure Sectors to Analyze:', font=("Arial", 12)).grid(row=1, sticky=tk.W, column = 4)
            tk.Checkbutton(self, text='Water', var=water_bool, font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 4)
            tk.Checkbutton(self, text='Energy', var=energy_bool, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 4)
            tk.Checkbutton(self, text='Transportation', var=transportation_bool, font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 4)
            tk.Checkbutton(self, text='Communications', var=comm_bool, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 4)
            tk.Checkbutton(self, text='Government', var=gov_bool, font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 4)
            tk.Checkbutton(self, text='Food/Agriculture', var=fa_bool, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 4)
            tk.Checkbutton(self, text='Emergency Services', var=emer_bool, font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 4)
            tk.Checkbutton(self, text='Waste Management', var=waste_bool, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 4)
            tk.Checkbutton(self, text='Healthcare', var=healthcare_bool, font=("Arial", 10)).grid(row=10, sticky=tk.W, column = 4)
            #print(self.orders, self.coeffs, self.k)
            tk.Button(self, text='Run Analysis', bg='#FCB1A0', command= lambda: saveValues(), font=("Arial", 14)).grid(row=18, column=0, sticky=tk.NSEW)
            tk.Button(self, text='Cancel', bg='#C0C0C0', command=self.destroy, font=("Arial", 14)).grid(row=18, column=1, sticky=tk.NSEW)
 
            
    

    global app
    app = TKinterWindow()
    app.title("Report")
    app.mainloop()

if __name__ == '__main__':

    def refresh():
        app.destroy()
        leg = main()
    leg = main()



