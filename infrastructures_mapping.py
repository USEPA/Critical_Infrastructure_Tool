# -*- coding: utf-8 -*-
"""
infrastructures_interactive_plotting.py
Created on Sun Aug 27 14:39:25 2019
Created by: Mitchell Wendt
Revised: 08/28/2019
Revised by: Mitchell Wendt
"""

import numpy as np
import warnings
import infrastructures_v4
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from osgeo import ogr

def loadMap(filename):
    hazus = gpd.read_file(r'C:\Repos\EPA\Shapefiles\harvey\houston data\HoustonBlocks.shp') ###Co to jest
    scenarioData = gpd.read_file(filename)
    base = hazus.plot(color='#e0ecf4', figsize=(40,40), legend=True, legend_kwds={'label': "Infrastructure Data"})
    #scenarioData.plot(ax=base, color='#8856a7', legend=True, legend_kwds={'label': "Incident Data"})
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    result = gpd.overlay(hazus, scenarioData, how='intersection')
    result.plot(ax=base, color='#d97582', legend=True, legend_kwds={'label': "Incident Data"})

    agr1 = result["agr1count"]
    agr1Total = hazus["agr1count"]
    agPercent = agr1/agr1Total
    com1 = result["com1count"]
    com1Total = hazus["com1count"]
    com1Percent = com1/com1Total
    com2 = result["com2count"]
    com2Total = hazus["com2count"]
    com2Percent = com2/com2Total
    com4 = result["com4count"]
    com4Total = hazus["com4count"]
    com4Percent = com4/com4Total
    com6 = result["com6count"]
    com6Total = hazus["com6count"]
    com6Percent = com6/com6Total
    com8 = result["com8count"]
    com8Total = hazus["com8count"]
    com8Percent = com8/com8Total
    edu1 = result["edu1count"]
    edu1Total = hazus["edu1count"]
    edu1Percent = edu1/edu1Total
    edu2 = result["edu2count"]
    edu2Total = hazus["edu2count"]
    edu2Percent = edu2/edu2Total
    res5 = result["res5count"]
    res5Total = hazus["res5count"]
    res5Percent = res5/res5Total
    res6 = result["res6count"]
    res6Total = hazus["res6count"]
    res6Percent = res6/res6Total
    gov1 = result["gov1count"]
    gov1Total = hazus["gov1total"]
    gov1Percent = gov1/gov1Total
    gov2 = result["gov2count"]
    gov2Total = hazus["gov2total"]
    gov2Percent = gov2/gov2Total

    water = (1- com4Percent)*100
    energy = (1-(com4Percent + com1Percent)/2)*100
    transport = (1-(com4Percent + com1Percent)/2)*100
    communication = (1-com8Percent)*100
    government = (1-(gov1Percent + gov2Percent + edu1Percent + edu2Percent)/4)*100
    food = (1-(com1Percent + agr1Percent)/2)*100
    emergency = (1-gov2Percent)*100
    healthcare = (1-(res6Percent + com6Percent + com7Percent)/3)*100

    return [water, energy, transport, communication, government, food, emergency, healthcare]

    
    plt.show()
