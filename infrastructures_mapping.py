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

def loadMap(filename):
    hazus = gpd.read_file(r'C:\Repos\EPA\Shapefiles\harvey\houston data\HoustonBlocks.shp')
    scenarioData = gpd.read_file(filename)
    base = hazus.plot(color='#e0ecf4', figsize=(40,40), legend=True, legend_kwds={'label': "Infrastructure Data"})
    scenarioData.plot(ax=base, color='#8856a7', legend=True, legend_kwds={'label': "Incident Data"})
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.show()
