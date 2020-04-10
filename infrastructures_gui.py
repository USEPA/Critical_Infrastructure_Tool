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
import os
if (sys.version_info > (3,0)):
  from tkinter.filedialog import askopenfilename
else:
  from tkFileDialog import askopenfilename

def main():
    LARGE_FONT= ("Verdana", 24)

    class TKinterWindow(tk.Tk):

        def __init__(self, *args, **kwargs):

            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)

            container.pack(side="top", fill="both", expand = True)

            container.grid_rowconfigure(11, weight=1)
            container.grid_columnconfigure(4, weight=1)

            self.frames = {}

            frame = StartPage(container, self)

            self.frames[StartPage] = frame

            frame.grid(row=1, column=1, sticky="nsew")

            self.geometry("1600x600")

            self.show_frame(StartPage)

        def show_frame(self, cont):

            frame = self.frames[cont]
            frame.tkraise()

    class StartPage(tk.Frame):

        def __init__(self, parent, controller):

            self.leg = None
            dirpath = os.getcwd()

            self.orders, self.coeffs, self.k = coefficients_from_file.load_file(dirpath + "//"+ "default.csv")
            #print(self.orders, self.coeffs, self.k)

            def run(optimize):
                f = open(dirpath + "//" + "infrastructures_inputs.txt", "w")
                f.write("n0 "+ str(var5.get())+"\n")
                f.write("p0 "+ str(var6.get())+"\n")
                f.write("repair_factors "+ str(var7.get())+"\n")
                f.write("nLoss "+ str(var8.get())+"\n")
                f.write("tLoss "+ str(var9.get())+"\n")
                f.write("timeSpan "+ str(var12.get())+"\n")
                f.write("nRun "+ str(var10.get())+"\n")
                f.write("paramTypes "+ str(var13.get())+"\n")
                f.write("paramIndexes "+ str(var14.get())+"\n")
                f.write("infStoichFactor "+ str(var15.get())+"\n")
                f.write("printProgress "+ str(bool(var1.get()))+"\n")
                f.write("averaging "+ str(bool(var2.get()))+"\n")
                f.write("intervals "+ str(bool(var3.get()))+"\n")
                f.write("agent "+ str(var4.get())+"\n")
                f.write("seedValue "+ str(var16.get())+"\n")
                f.write("name "+ str(var17.get())+"\n")
                f.write("remediationFactor "+ str(var18.get())+"\n")
                f.write("contamination "+ str(var19.get())+"\n")
                f.write("maxPercent "+ str(var20.get())+"\n")
                f.write("backups "+ str(var21.get())+"\n")
                f.write("backupPercent "+ str(var22.get())+"\n")
                f.write("daysBackup "+ str(var23.get())+"\n")
                f.write("depBackup "+ str(var24.get())+"\n")
                f.close()
                self.leg = infrastructures_from_file.run_file(optimize, self.orders, self.coeffs, self.k)
                if optimize:
                    print(self.leg)

            def loadCoeff():
                filename = askopenfilename()
                self.orders, self.coeffs, self.k = coefficients_from_file.load_file(filename)
                

            n0, p0, repair_factors, nLoss, tLoss, timeSpan, nRun, paramTypes, paramIndexes, printProgress, averaging, confIntervals, infStoichFactor, agent, seedValue, name, remediationFactor, contaminated, maxPercent, backups, backupPercent, daysBackup, depBackup = infrastructures_from_file.read_file()

            mainframe = tk.Frame.__init__(self,parent)
            label = tk.Label(self, text="Start Page", font=LARGE_FONT)
            label.grid(row=0, sticky=tk.NSEW, columnspan=4)

            #Checkboxes
            if printProgress == "true" or printProgress == "True" or printProgress == "1":
                var1 = tk.IntVar(value=int(bool(printProgress)))
            else:
                var1 = tk.IntVar()
            tk.Checkbutton(self, text="Print Progress", variable=var1).grid(row=1, sticky=tk.W)

            if averaging == "true" or averaging == "True" or averaging == "1":
                var2 = tk.IntVar(value=int(bool(averaging)))
            else:
                var2 = tk.IntVar()
            tk.Checkbutton(self, text="Run-average", variable=var2).grid(row=2, sticky=tk.W)

            if confIntervals == "true" or confIntervals == "True" or confIntervals == "1":
                var3 = tk.IntVar(value=int(bool(confIntervals)))
            else:
                var3 = tk.IntVar()
            tk.Checkbutton(self, text="Confidence Intervals", variable=var3).grid(row=3, sticky=tk.W)

            #String Parameters
            tk.Label(self, text="Agent: ").grid(row=4, column = 0, sticky=tk.W)
            var4 = tk.StringVar()
            choices = ['anthrax','ebola','monkeypox', 'natural_disaster']
            var4.set(agent)
            defaulut_agent = agent
            Agent = tk.OptionMenu(self, var4, *choices)
            Agent.grid(row=4, column = 1)
            def change_dropdown(choice, foo, bar):
                default_agent = choice
            var4.trace('w', change_dropdown)

            #String Parameters
            tk.Label(self, text="Initial infrastructure sector efficiencies (%): ").grid(row=5, column = 0, sticky=tk.W)
            var5 = tk.StringVar()
            N0 = tk.Entry(self, textvariable=var5)
            N0.insert(0, n0)
            N0.grid(row=5, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Initial contaminated infrastructure (%): ").grid(row=8, column = 0, sticky=tk.W)
            var19 = tk.StringVar()
            C0 = tk.Entry(self, textvariable=var19)
            C0.insert(0, contaminated)
            C0.grid(row=8, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Initial populations: ").grid(row=6, column = 0, sticky=tk.W)
            var6 = tk.StringVar()
            P0 = tk.Entry(self, textvariable=var6)
            P0.insert(0, p0)
            P0.grid(row=6, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Repair Factors: ").grid(row=7, column = 0, sticky=tk.W)
            var7 = tk.StringVar()
            Repair_factors = tk.Entry(self, textvariable=var7)
            Repair_factors.insert(0, repair_factors)
            Repair_factors.grid(row=7, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Remediation Factor (%/day): ").grid(row=9, column = 0, sticky=tk.W)
            var18 = tk.StringVar()
            Remediation_factor = tk.Entry(self, textvariable=var18)
            Remediation_factor.insert(0, remediationFactor)
            Remediation_factor.grid(row=9, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Amounts of additional infrastructure outages (if applicable, %): ").grid(row=10, column = 0, sticky=tk.W)
            var8 = tk.StringVar()
            NLoss = tk.Entry(self, textvariable=var8)
            NLoss.insert(0, nLoss)
            NLoss.grid(row=10, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Time of additional infrastructure outages (if applicable, days): ").grid(row=1, column = 2, sticky=tk.W)
            var9 = tk.StringVar()
            TLoss = tk.Entry(self, textvariable=var9)
            TLoss.insert(0, tLoss)
            TLoss.grid(row=1, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Number of stochastic runs:").grid(row=2, column = 2, sticky=tk.W)
            var10 = tk.StringVar()
            NRun = tk.Entry(self, textvariable=var10)
            NRun.insert(0, nRun)
            NRun.grid(row=2, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Simulation Length (days): ").grid(row=3, column = 2, sticky=tk.W)
            var12 = tk.StringVar()
            TimeSpan = tk.Entry(self, textvariable=var12)
            TimeSpan.insert(0, timeSpan)
            TimeSpan.grid(row=3, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Parameters to be collected (min, max, average, recover_time, and final_val): ").grid(row=4, column = 2, sticky=tk.W)
            var13 = tk.StringVar()
            ParamTypes = tk.Entry(self, textvariable=var13)
            ParamTypes.insert(0, paramTypes)
            ParamTypes.grid(row=4, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Infrastructure indexes of parameters: ").grid(row=5, column = 2, sticky=tk.W)
            var14 = tk.StringVar()
            ParamIndexes = tk.Entry(self, textvariable=var14)
            ParamIndexes.insert(0, paramIndexes)
            ParamIndexes.grid(row=5, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Infrastructure Stoichiometric Factor: ").grid(row=6, column = 2, sticky=tk.W)
            var15 = tk.StringVar()
            InfStoichFactor = tk.Entry(self, textvariable=var15)
            InfStoichFactor.insert(0, infStoichFactor)
            InfStoichFactor.grid(row=6, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Seed: ").grid(row=7, column = 2, sticky=tk.W)
            var16 = tk.StringVar()
            SeedValue = tk.Entry(self, textvariable=var16)
            SeedValue.insert(0, seedValue)
            SeedValue.grid(row=7, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Maximum Percent: ").grid(row=9, column = 2, sticky=tk.W)
            var20 = tk.StringVar()
            PercentValue = tk.Entry(self, textvariable=var20)
            PercentValue.insert(0, maxPercent)
            PercentValue.grid(row=9, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Results Chart Name: ").grid(row=8, column = 2, sticky=tk.W)
            var17 = tk.StringVar()
            ChartName = tk.Entry(self, textvariable=var17)
            ChartName.insert(0, name)
            ChartName.grid(row=8, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Backup infrastructure indexes of parameters: ").grid(row=11, column = 0, sticky=tk.W)
            var21 = tk.StringVar()
            Backup = tk.Entry(self, textvariable=var21)
            Backup.insert(0, backups)
            Backup.grid(row=11, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Backup infrastructure efficiency (%): ").grid(row=12, column = 0, sticky=tk.W)
            var22 = tk.StringVar()
            BackupPercent = tk.Entry(self, textvariable=var22)
            BackupPercent.insert(0, backupPercent)
            BackupPercent.grid(row=12, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Days backup is available: ").grid(row=13, column = 0, sticky=tk.W)
            var23 = tk.StringVar()
            BackupDays = tk.Entry(self, textvariable=var23)
            BackupDays.insert(0, daysBackup)
            BackupDays.grid(row=13, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Dependant infrastructure indexes of parameters:  ").grid(row=14, column = 0, sticky=tk.W)
            var24 = tk.StringVar()
            DepBackup = tk.Entry(self, textvariable=var24)
            DepBackup.insert(0, depBackup)
            DepBackup.grid(row=14, column = 1, sticky=tk.NSEW)
            
            #Index Note
            note = tk.Label(self, text="Infrastructure indexes (used in initial infrastructure sector efficiencies, repair factors, " \
                                        "and infrastructure indexes of parameters) are water (0), energy (1), transport services (2), " \
                                        "\ncommunications services (3), government facilities (4), food and agriculture (5), emergency services " \
                                        "(6), waste management (7),  healthcare (8)", #healthcare (9), \nchemical (10), " \
                                        #"commercial facilities (11), manufacturing (12), dams (13), defense (14), and nuclear (15).", \
                                        font=("Verdana", 7))
            note.grid(row=17, column = 0, columnspan = 4, sticky=tk.NSEW)

            #Buttons

            tk.Button(self, text='Run', command= lambda: run(False)).grid(row=15, column=0, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Quit', command=self.destroy).grid(row=15, column=2, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Load Coefficients', command= lambda: loadCoeff()).grid(row=19, column=0, sticky=tk.NSEW, columnspan=2)
            #tk.Button(self, text='Optimize', command= lambda: run(True)).grid(row=13, column=0, sticky=tk.NSEW, columnspan=2)

            #GUI Spacing
            for i in range(1,9):
                self.grid_rowconfigure(i, weight=1, uniform="foo")
            for i in range(0,4):
                self.grid_columnconfigure(i, weight=1, uniform="bar")

    app = TKinterWindow()
    app.title("Battelle-Gillespie Infrastructure Model")
    app.mainloop()

if __name__ == '__main__':
    leg = main()
