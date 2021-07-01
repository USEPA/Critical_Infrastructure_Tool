# -*- coding: utf-8 -*-
"""
infrastructures_prioritization.py
Created on Aug 28 14:06:28 2019
Created by: Mitchell Wendt
Revised: 08/28/2019
Revised by: Mitchell Wendt
"""

import numpy as np
from more_itertools import sort_together

def get_sector_name(sector):
    if sector == 0:
        return "Water and Wastewater Systems"
    elif sector == 1:
        return "Energy"
    elif sector == 2:
        return "Transportation Systems"
    elif sector == 3:
        return "Communications"
    elif sector == 4:
        return "Government Facilities"
    elif sector == 5:
        return "Food and Agriculture"
    elif sector == 6:
        return "Emergency Services"
    elif sector == 7:
        return "Waste Management"


def prioritizations(t, n, orders, lower_bounds, upper_bounds, weightings):

    scores = np.zeros([8], dtype=float)
    loss_time = np.zeros([8], dtype=float)
    connectivity = np.zeros([8], dtype=float)
    #connectivity defined as sum of children subsectors
    orders = np.transpose(orders)
    for i in range(0, len(connectivity)):
        connectivity[i] = sum(orders[i])
    for i in range(1, len(n)):
        for j in range(0, len(n[i])):
            if (t[i]-t[i-1])*(100.0-n[i][j]) > 0:
                loss_time[j] += (t[i]-t[i-1])*(100.0-n[i][j])
    for i in range(0, len(scores)):
        scores[i] = loss_time[i]*connectivity[i]*weightings[i]
        if lower_bounds is not None and upper_bounds is not None:
            scores[i] = scores[i] * (upper_bounds[-1][i] - lower_bounds[-1][i])
    indices = np.array([0,1,2,3,4,5,6,7])
    sectors = np.flip(sort_together([scores,indices])[1])
    print("")
    print("Infrastructure prioritizations:")
    for i in range(0,len(sectors)):
        print(str(i+1) + ". " + get_sector_name(sectors[i]))

    indices = np.array([0,1,2,3,4,5,6,7])
    sectors = np.flip(sort_together([loss_time,indices])[1])
    print("")
    print("In decreasing order by loss time:")
    for i in range(0,len(sectors)):
        print(str(i+1) + ". " + get_sector_name(sectors[i]))
