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

def main():
    LARGE_FONT= ("Verdana", 24)

    class TKinterWindow(tk.Tk):

        def __init__(self, *args, **kwargs):

            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)

            container.pack(side="top", fill="both", expand = True)

            container.grid_rowconfigure(20, weight=1)
            container.grid_columnconfigure(2, weight=1)

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
            
            def saveValues():
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
                
            self.leg = None
            
            #bool definitions
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

            tk.Checkbutton(self, text='Show Water Sensitivity', var=water_bool, font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Show Water Recovery Histogram', var=water_graph_bool, font=("Arial", 10)).grid(row=2, sticky=tk.W, column = 1)

            tk.Checkbutton(self, text='Show Energy Sensitivity', var=energy_bool, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Show Energy Recovery Histogram', var=energy_graph_bool, font=("Arial", 10)).grid(row=3, sticky=tk.W, column = 1)

            tk.Checkbutton(self, text='Show Transportation Sensitivity', var=transportation_bool, font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Show Transportation Recovery Histogram', var=transportation_graph_bool, font=("Arial", 10)).grid(row=4, sticky=tk.W, column = 1)

            tk.Checkbutton(self, text='Show Communications Sensitivity', var=comm_bool, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Show Communications Recovery Histogram', var=comm_graph_bool, font=("Arial", 10)).grid(row=5, sticky=tk.W, column = 1)

            tk.Checkbutton(self, text='Show Government Sensitivity', var=gov_bool, font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Show Government Recovery Histogram', var=gov_graph_bool, font=("Arial", 10)).grid(row=6, sticky=tk.W, column = 1)

            tk.Checkbutton(self, text='Show Food/Agriculture Sensitivity', var=fa_bool, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Show Food/Agriculture Recovery Histogram', var=fa_graph_bool, font=("Arial", 10)).grid(row=7, sticky=tk.W, column = 1)

            tk.Checkbutton(self, text='Show Emergency Services Sensitivity', var=emer_bool, font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Show Emergency Services Recovery Histogram', var=emer_graph_bool, font=("Arial", 10)).grid(row=8, sticky=tk.W, column = 1)

            tk.Checkbutton(self, text='Show Waste Management Sensitivity', var=waste_bool, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Show Waste Management Recovery Histogram', var=waste_graph_bool, font=("Arial", 10)).grid(row=9, sticky=tk.W, column = 1)

            tk.Checkbutton(self, text='Show Healthcare Sensitivity', var=healthcare_bool, font=("Arial", 10)).grid(row=10, sticky=tk.W, column = 0)
            tk.Checkbutton(self, text='Show Healthcare Recovery Histogram', var=healthcare_graph_bool, font=("Arial", 10)).grid(row=10, sticky=tk.W, column = 1)            
            #print(self.orders, self.coeffs, self.k)

            tk.Button(self, text='Save Report Values', bg='#FCB1A0', command= lambda: saveValues(), font=("Arial", 14)).grid(row=18, column=0, sticky=tk.NSEW)
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



