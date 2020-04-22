# -*- coding: utf-8 -*-
"""
infrastructures_results.py
Created on Sun Aug 27 14:23:05 2019
Created by: Mitchell Wendt
Revised: 08/28/2019
Revised by: Mitchell Wendt
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statistics
from scipy.stats import kurtosis, skew

# def results(t, n, p, nRun, timeSpan, averages, bin_size, paramTypes, paramIndexes, param_vals, agent):
def results(nRun, paramTypes, paramIndexes, param_vals, runName, contam, maxTime):

    #Plot histograms if relevant
    if nRun > 1 and paramTypes is not None and paramIndexes is not None:

        for i in range(0,len(paramTypes)):
            plt.figure(figsize=(17,8))
            plt.hist(param_vals[i], range=[0, maxTime])

            #fetch sector name and parameter name for title
            if paramTypes[i] == 'min':
                param_name = 'Minimum (%)'
            elif paramTypes[i] == 'max':
                param_name = 'Maximum (%)'
            elif paramTypes[i] == 'average':
                param_name = 'Average (%)'
            elif paramTypes[i] == 'recover_time':
                param_name = 'Sector Recovery Time (Days)'
            else:
                param_name = 'Final Value (%)'

            if paramIndexes[i] == 0:
                sector_name = "Water"
            elif paramIndexes[i] == 1:
                sector_name = "Energy"
            elif paramIndexes[i] == 2:
                sector_name = "Transportation"
            elif paramIndexes[i] == 3:
                sector_name = "Communication"
            elif paramIndexes[i] == 4:
                sector_name = "Government"
            elif paramIndexes[i] == 5:
                sector_name = "Food"
            elif paramIndexes[i] == 6:
                sector_name = "Emergency Services"
            elif paramIndexes[i] == 7:
                sector_name = "Waste"

            #set titles and axes labels of second plot
            plt.rcParams.update({'font.size': 22})
            plt.title('Parameter Histogram: ' + param_name + ' of ' + sector_name + ' Sector Efficiency')
            plt.xlabel('Parameter Value')
            plt.ylabel('Frequency of Parameter Range')
            plt.savefig("Images/" + runName + " " + sector_name)
            #print out distribution statistics as desired
            print("")
            print(param_name + ' of ' + sector_name + ' Sector Efficiency')
            print("Average: "+str(statistics.mean(param_vals[i])))
            print("Sample SD: "+str(statistics.stdev(param_vals[i])))
            print("Min: "+str(min(param_vals[i])))
            percentiles = np.array([0.1, 1, 2.5, 5, 10, 25, 50, 75, 90, 95, 97.5, 99, 99.9])
            for j in percentiles:
                print("Percentile " + str(j) + ": " + str(np.percentile(param_vals[i], j)))
            print("Max: "+str(max(param_vals[i])))
            print("Skewness: "+str(skew(param_vals[i])))
            print("Kurtosis: "+str(kurtosis(param_vals[i])))

    #Plot disease outbreak time profiles if applicable (healthy people, sick people, immune people, dead people)
    # if max(p[:,1]) > 1:
    #     plt.figure(figsize=(17,8))

    #     #skip plotting the number of healthy people if only a small number get sick
    #     if max(p[:,1]) > 50000:
    #         plt.plot(t, p[:,0], color = 'blue', label = 'healthy')
    #     plt.plot(t, p[:,1], color = 'red', label = 'sick')
    #     plt.plot(t, p[:,2], color = 'green', label = 'immune')
    #     plt.plot(t, p[:,3], color = 'black', label = 'dead')
    #     plt.title('Example Disease Outbreak Time Profile (Run #'+ str(nRun)+')')
    #     plt.xlabel('t (days)')
    #     plt.ylabel('People')
    #     plt.legend()
    #     axes = plt.gca()
    #     axes.set_xlim([0,timeSpan])
    #     if agent == "ebola":
    #         axes.set_ylim([0,sum(p[0])])
    #     elif agent == "monkeypox":
    #         axes.set_ylim([0,max(p[:,2])])
    #     else:
    #         axes.set_ylim([0,max(p[:,1])])
