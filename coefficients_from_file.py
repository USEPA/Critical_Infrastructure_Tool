# -*- coding: utf-8 -*-
"""
coefficients_from_file.py
Created in March

"""

import numpy as np
import warnings
import infrastructures_v4
import pandas as pd
import tkinter.messagebox as tkMessageBox
import os
from os.path import abspath
from inspect import getsourcefile

def load_file(filename):
    dir_path = os.path.dirname(abspath(getsourcefile(lambda:0)))
    data = pd.read_csv("default.csv")
    sectors = data["Sector"]
    numSectors = 9
    finalCoeffs = np.array([[0.0 for x in range(numSectors)] for y in range(numSectors)])
    finalOrders = np.array([[0.0 for x in range(numSectors)] for y in range(numSectors)])
    kArray = np.array([[0.0 for x in range(numSectors)] for y in range(numSectors)])
    ks = np.array([0.0 for x in range(numSectors)])
    maxVal = 0
    try:
        for s in range(0,numSectors):
            coeffs = data[sectors[s]]
            for c in range(0,len(coeffs)):
                coeff = coeffs[c]
                if coeff>maxVal:
                    maxVal = coeff
                if coeff < 0:
                    tkMessageBox.showerror("Error","Coefficients must be positive")
                    raise ValueError("Coefficients must be positive")
                finalOrders[s][c] = coeff
                if s == c:
                    finalCoeffs[s][c] = 0
                else:
                    finalCoeffs[s][c] = -coeff
        resultOrder = np.divide(finalOrders, maxVal)
        print(maxVal)
        for s in range(0,numSectors):
            coeff = -sum(finalCoeffs[s])
            finalCoeffs[s][s] = coeff
        resultCoeffs = np.divide(finalCoeffs, maxVal)

        for row in range(0, numSectors):
            for col in range(0,numSectors):
                kArray[row][col] = 100**resultOrder[row][col]

        for s in range(0,numSectors):
            ks[s] = 100/np.product(kArray[s])
    except:
        tkMessageBox.showerror("Error","Ensure the 9 sectors are named properly. Check default.csv for the proper format")
        raise ValueError("Ensure the sectors are named properly and are the correct values")

    return resultOrder, resultCoeffs, ks

if __name__ == '__main__':
    leg = run_file()
