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
import tkinter.messagebox as tkMessageBox
import infrastructures_mapping
import json
import os
if (sys.version_info > (3,0)):
  from tkinter.filedialog import askopenfilename
else:
  from tkFileDialog import askopenfilename


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

def main():
    LARGE_FONT= ("Verdana", 24)

    class TKinterWindow(tk.Tk):

        def __init__(self, *args, **kwargs):

            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)

            container.pack(side="top", fill="both", expand = True)

            container.grid_rowconfigure(20, weight=1)
            container.grid_columnconfigure(4, weight=1,minsize="600")

            self.frames = {}

            frame = StartPage(container, self)

            self.frames[StartPage] = frame

            frame.grid(row=1, column=1, sticky="nsew")

            self.geometry("1200x700")
            

            self.show_frame(StartPage)

        def show_frame(self, cont):
            
            frame = self.frames[cont]
            #frame.config(bg="#F7FCF6")
            frame.tkraise()

    class StartPage(tk.Frame):

        def __init__(self, parent, controller):

            self.leg = None
            dirpath = os.getcwd()

            self.orders, self.coeffs, self.k = coefficients_from_file.load_file(dirpath + "//"+ "default.csv")
            #print(self.orders, self.coeffs, self.k)

            def run(optimize):
                data = {}
                data["n0"] = var5.get().split(" ")
                data["p0"] = var6.get().split(" ")
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
                data["agent"] = var4.get()
                data["seedValue"] = var16.get()
                data["name"] = var17.get()
                data["remediationFactor"] = var18.get().split(" ")
                data["contamination"] = var19.get().split(" ")
                data["backups"] = var21.get().split(" ")
                data["backupPercent"] = var22.get().split(" ")
                data["daysBackup"] = var23.get().split(" ")
                data["depBackup"] = var24.get().split(" ")
                data["negatives"] = var25.get()
                fileLoc = dirpath + "//" + "infrastructure_inputs.txt"
                with open(fileLoc, "w") as outfile:
                    json.dump(data, outfile)
                self.leg = infrastructures_from_file.run_file(optimize, self.orders, self.coeffs, self.k)
                if optimize:
                    print(self.leg)
                    
            def runLoaded():
                print("opening folder")
                filename = askopenfilename()
                if ".txt" in filename:
                    n0, p0, repair_factors, nLoss, tLoss, timeSpan, nRun, paramTypes, paramIndexes, printProgress, averaging, \
                    confIntervals, infStoichFactor, agent, seedValue, name, remediationFactor, contaminated, backups, \
                    backupPercent, daysBackup, depBackup, negatives = infrastructures_from_file.read_file(filename)
                    json_data = open(filename)
                    data = json.load(json_data)
                    with open(dirpath + "//" + "infrastructure_inputs.txt", 'w') as outfile:
                        json.dump(data, outfile)
                    refresh()
                
            def loadCoeff():
                filename = askopenfilename()
                if ".csv" in filename:
                    self.orders, self.coeffs, self.k = coefficients_from_file.load_file(filename)
                else:
                    tkMessageBox.showerror("Error","Must be CSV file")

            def openGIS():
                filename = askopenfilename()
                if ".shp" in filename:
                    infrastructures_mapping.loadMap(filename)
                else:
                    tkMessageBox.showerror("Error","Must be shapefile")

            def loadInits():
                filename = askopenfilename()
                self.orders, self.coeffs, self.k = efficiencies_from_file.load_file(filename)
                
                
            n0, p0, repair_factors, nLoss, tLoss, timeSpan, nRun, paramTypes, paramIndexes, printProgress, averaging, \
                confIntervals, infStoichFactor, agent, seedValue, name, remediationFactor, contaminated, backups, \
                backupPercent, daysBackup, depBackup, negatives = infrastructures_from_file.read_file()
            

            mainframe = tk.Frame.__init__(self,parent)
            label = tk.Label(self, text="Start Page", font=("Arial", 40))
            label.grid(row=0, sticky=tk.NSEW, columnspan=4)

            #Checkboxes
            if printProgress == "true" or printProgress == "True" or printProgress == "1":
                var1 = tk.IntVar(value=int(bool(printProgress)))
            else:
                var1 = tk.IntVar()
            tk.Checkbutton(self, text="Print Progress", variable=var1, font=("Arial", 10)).grid(row=12, sticky=tk.W)

            if averaging == "true" or averaging == "True" or averaging == "1":
                var2 = tk.IntVar(value=int(bool(averaging)))
            else:
                var2 = tk.IntVar()
            tk.Checkbutton(self, text="Run-average", variable=var2, font=("Arial", 10)).grid(row=13, sticky=tk.W)
            
            if confIntervals == "true" or confIntervals == "True" or confIntervals == "1":
                var3 = tk.IntVar(value=int(bool(confIntervals)))
            else:
                var3 = tk.IntVar()
            tk.Checkbutton(self, text="Confidence Intervals", variable=var3, font=("Arial", 10)).grid(row=14, sticky=tk.W)

            #String Parameters
            tk.Label(self, text="Agent: ", font=("Arial", 10)).grid(row=1, column = 0, sticky=tk.W)
            var4 = tk.StringVar()
            choices = ['anthrax','ebola','monkeypox', 'natural_disaster']
            var4.set(agent)
            defaulut_agent = agent
            Agent = tk.OptionMenu(self, var4, *choices)
            Agent_ttp = CreateToolTip(Agent, 'Select the agent that the scenario will model')
            Agent.grid(row=1, column = 1)
            def change_dropdown(choice, foo, bar):
                default_agent = choice
            var4.trace('w', change_dropdown)

            #String Parameters
            tk.Label(self, text="Initial infrastructure sector efficiencies (%): ", font=("Arial", 10)).grid(row=2, column = 0, sticky=tk.W)
            var5 = tk.StringVar()
            N0 = tk.Entry(self, textvariable=var5)
            N0.insert(0, n0)
            N0_ttp = CreateToolTip(N0, 'Enter the efficiency of each infrastructure, each followed by a space. Use the order defined at the bottom.')
            N0.grid(row=2, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Initial contaminated infrastructure (%): ", font=("Arial", 10)).grid(row=3, column = 0, sticky=tk.W)
            var19 = tk.StringVar()
            C0 = tk.Entry(self, textvariable=var19)
            C0.insert(0, contaminated)
            C0_ttp = CreateToolTip(C0, 'Enter the percentage of each infrastructure contaminated, each followed by a space. Use the order defined at the bottom. ')
            C0.grid(row=3, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Initial populations: ", font=("Arial", 10)).grid(row=4, column = 0, sticky=tk.W)
            var6 = tk.StringVar()
            P0 = tk.Entry(self, textvariable=var6)
            P0_ttp = CreateToolTip(P0, 'Enter the population in the scenario area, the population sick and... ')
            P0.insert(0, p0)
            P0.grid(row=4, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Repair Factors: ", font=("Arial", 10)).grid(row=5, column = 0, sticky=tk.W)
            var7 = tk.StringVar()
            Repair_factors = tk.Entry(self, textvariable=var7)
            Repair_factors_ttp = CreateToolTip(Repair_factors, 'Enter the repair factor of each infrastructure, each followed by a space. Use the order defined at the bottom. ')
            Repair_factors.insert(0, repair_factors)
            Repair_factors.grid(row=5, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Remediation Factor (%/day): ", font=("Arial", 10)).grid(row=6, column = 0, sticky=tk.W)
            var18 = tk.StringVar()
            Remediation_factor = tk.Entry(self, textvariable=var18)
            Remediation_factor_ttp = CreateToolTip(Remediation_factor, 'Enter the % decontaminated per day of each infrastructure, each followed by a space. Use the order defined at the bottom')
            Remediation_factor.insert(0, remediationFactor)
            Remediation_factor.grid(row=6, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Amounts of additional infrastructure outages \n(if applicable, %): ", font=("Arial", 10)).grid(row=7, column = 0, sticky=tk.W)
            var8 = tk.StringVar()
            NLoss = tk.Entry(self, textvariable=var8)
            NLoss_ttp = CreateToolTip(NLoss, 'Enter additional percent outages')
            NLoss.insert(0, nLoss)
            NLoss.grid(row=7, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Time of additional infrastructure outages \n(if applicable, days): ", font=("Arial", 10)).grid(row=9, column = 2, sticky=tk.W)
            var9 = tk.StringVar()
            TLoss = tk.Entry(self, textvariable=var9)
            TLoss_ttp = CreateToolTip(TLoss, 'Enter additional time outage')
            TLoss.insert(0, tLoss)
            TLoss.grid(row=9, column = 3, sticky=tk.NSEW)

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

            tk.Label(self, text="Parameters to be collected (min, max, average, \nrecover_time(write rt in entry box), final_val): ", font=("Arial", 10)).grid(row=4, column = 2, sticky=tk.W)
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

            tk.Label(self, text="Results Chart Name: ", font=("Arial", 10)).grid(row=8, column = 2, sticky=tk.W)
            var17 = tk.StringVar()
            ChartName = tk.Entry(self, textvariable=var17)
            ChartName_ttp = CreateToolTip(ChartName, 'Enter the name of the scenario (no spaces)')
            ChartName.insert(0, name)
            ChartName.grid(row=8, column = 3, sticky=tk.NSEW)

            tk.Label(self, text="Backup infrastructure indexes of parameters: ", font=("Arial", 10)).grid(row=8, column = 0, sticky=tk.W)
            var21 = tk.StringVar()
            Backup = tk.Entry(self, textvariable=var21)
            Backup_ttp = CreateToolTip(Backup, 'Enter the index of any backup infrastructures, each followed by a space. Keep the same order between the backup inputs. You will need to have individual entries for each dependant infrastructure, even if the same infrastructure is a backup')
            Backup.insert(0, backups)
            Backup.grid(row=8, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Backup infrastructure efficiency (%): ", font=("Arial", 10)).grid(row=9, column = 0, sticky=tk.W)
            var22 = tk.StringVar()
            BackupPercent = tk.Entry(self, textvariable=var22)
            BackupPercent_ttp = CreateToolTip(BackupPercent, 'Enter the percent efficiency of any backup infrastructures, each followed by a space. Keep the same order between the backup inputs. You will need to have individual entries for each dependant infrastructure, even if the same infrastructure is a backup')
            BackupPercent.insert(0, backupPercent)
            BackupPercent.grid(row=9, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Days backup is available: ", font=("Arial", 10)).grid(row=10, column = 0, sticky=tk.W)
            var23 = tk.StringVar()
            BackupDays = tk.Entry(self, textvariable=var23)
            BackupDays_ttp = CreateToolTip(BackupDays, 'Enter the number of days the backup is available for each dependant infrastructure, each followed by a space. Keep the same order between the backup inputs. You will need to have individual entries for each dependant infrastructure, even if the same infrastructure is a backup')
            BackupDays.insert(0, daysBackup)
            BackupDays.grid(row=10, column = 1, sticky=tk.NSEW)

            tk.Label(self, text="Dependant infrastructure indexes of parameters: ", font=("Arial", 10)).grid(row=11, column = 0, sticky=tk.W)
            var24 = tk.StringVar()
            DepBackup = tk.Entry(self, textvariable=var24)
            DepBackup_ttp = CreateToolTip(DepBackup, 'Enter the indexes of the infrastructures dependant on the above backups. Keep the same order between the backup inputs')
            DepBackup.insert(0, depBackup)
            DepBackup.grid(row=11, column = 1, sticky=tk.NSEW)
            
            #Index Note
            note = tk.Label(self, text="Infrastructure indexes (used in initial infrastructure sector efficiencies, repair factors, " \
                                        "and infrastructure indexes of parameters) are water (0), energy (1), transport services (2), " \
                                        "\ncommunications services (3), government facilities (4), food and agriculture (5), emergency services " \
                                        "(6), waste management (7),  healthcare (8)", #healthcare (9), \nchemical (10), " \
                                        #"commercial facilities (11), manufacturing (12), dams (13), defense (14), and nuclear (15).", \
                                        font=("Arial Bold", 10), bg='#F9F8E5', borderwidth=2, relief="groove")
            note.grid(row=19, column = 0, columnspan = 4, sticky=tk.NSEW)

            #Buttons

            if negatives == "true" or negatives == "True" or negatives == "1":
                var25 = tk.IntVar(value=int(bool(negatives)))
            else:
                var25 = tk.IntVar()
            tk.Checkbutton(self, text='Reduce Parent Efficiency', var=var25, font=("Arial", 10)).grid(row=15, sticky=tk.W)

            tk.Button(self, text='Run GUI Scenario',bg='#C7FCA0',command= lambda: run(False), font=("Arial", 14)).grid(row=14, column=2, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Quit', bg='#FCB1A0', command=self.destroy, font=("Arial", 14)).grid(row=15, column=2, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Load Coefficients', font=("Arial", 14), bg='#A0D4FC', command= lambda: loadCoeff()).grid(row=13, column=2, sticky=tk.NSEW, columnspan=2)
            #tk.Button(self, text='Load GIS Data', font=("Arial", 14), bg='#bcbddc', command= lambda: openGIS()).grid(row=12, column=2, sticky=tk.NSEW, columnspan=2)
            tk.Button(self, text='Load Scenario', font=("Arial", 14), bg='#bcbddc', command= lambda: runLoaded()).grid(row=12, column=2, sticky=tk.NSEW, columnspan=2)
            #tk.Button(self, text='Optimize', command= lambda: run(True)).grid(row=13, column=0, sticky=tk.NSEW, columnspan=2)

            #GUI Spacing
            for i in range(1,9):
                self.grid_rowconfigure(i, weight=1, uniform="foo")
            for i in range(0,4):
                self.grid_columnconfigure(i, weight=1, uniform="bar")

    global app
    app = TKinterWindow()
    app.title("Battelle-Gillespie Infrastructure Model")
    app.mainloop()

if __name__ == '__main__':

    def refresh():
        app.destroy()
        leg = main()
    leg = main()



