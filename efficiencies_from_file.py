# -*- coding: utf-8 -*-
"""
infrastructures_from_file.py
Created on Wed Jun 19 15:12:06 2019
"""

import numpy as np
import warnings
import infrastructures_v4
import pandas as pd

def load_file(filename):
    data = pd.read_csv(filename)
    sectors = data["Sector"]
    numSectors = len(sectors)
    initialEfficiencies = data["Efficiencies"][:9]
    repairFactors = data["Repair"][:9]
    initialContamination = data["Contamination"][:9]

    return initialEfficiencies, repairFactors, initialContamination

if __name__ == '__main__':
    leg = run_file()
