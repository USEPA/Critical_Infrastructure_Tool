# -*- coding: utf-8 -*-
"""
infrastructures_from_file.py
Created on Wed Jun 19 15:12:06 2019
Created by: Mitchell Wendt
Revised: 08/28/2019
Revised by: Mitchell Wendt
"""

import numpy as np
import warnings
import infrastructures_v4
import tkinter.messagebox as tkMessageBox
import json
import os
from inspect import getsourcefile
from os.path import abspath

        
def read_file(fname = "infrastructures_inputs.txt"):

    #This function is only used by infrastructures_gui to prepopulate the entry boxes in the GUI

    #read file
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_data = open(fname)
    data = json.load(json_data)
    contamString = data["contamination"]

    return contamString

def run_file(fname = "infrastructures_inputs.txt"):
    contaminated = read_file(fname)
    newPath = wrapArg(GUI_Tool_Location +  "\\infrastructures_gui.exe")
    command_prompt = "cmd /k " + newPath
    os.system(command_prompt)

if __name__ == '__main__':
    leg = run_file()
