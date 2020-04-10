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
import pandas as pd

def load_file(filename):
    data = pd.read_csv(filename)
    sectors = data["Sector"]
    numSectors = len(sectors)
    finalCoeffs = np.array([[0.0 for x in range(numSectors)] for y in range(numSectors)])
    finalOrders = np.array([[0.0 for x in range(numSectors)] for y in range(numSectors)])
    kArray = np.array([[0.0 for x in range(numSectors)] for y in range(numSectors)])
    ks = np.array([0.0 for x in range(numSectors)])
    maxVal = 0
    for s in range(0,numSectors):
        coeffs = data[sectors[s]]
        for c in range(0,len(coeffs)):
            coeff = coeffs[c]
            if coeff>maxVal:
                maxVal = coeff
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

    return resultOrder, resultCoeffs, ks

if __name__ == '__main__':
    leg = run_file()
