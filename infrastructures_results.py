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
import json
from scipy.stats import kurtosis, skew
import os
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
            elif paramIndexes[i] == 8:
                sector_name = "Healthcare"
           

            #set titles and axes labels of second plot
            plt.rcParams.update({'font.size': 22})
            plt.title('Parameter Histogram: ' + param_name + ' of ' + sector_name + ' Sector Efficiency')
            plt.xlabel('Parameter Value')
            plt.ylabel('Frequency of Parameter Range')
            
            if not os.path.exists("Images"):
                os.makedirs("Images")
            if not os.path.exists("Results"):
                os.makedirs("Results")
            plt.savefig("Images/" + runName + " " + sector_name)
            plt.close()
            #print out distribution statistics as desired
            print("")
            master_path = os.path.dirname(os.path.abspath('final_pdf.py'))
            filePath=master_path+'\\'+'path'+'.json'
            with open(filePath) as f:
                path=json.load(f)
            if path['change']==0:
                f = open("Results/" + runName + " " + sector_name + ".txt", "w")
                print(param_name + ' of ' + sector_name + ' Sector Efficiency')
                f.write(param_name + ' of ' + sector_name + ' Sector Efficiency \n')
                print("Average: "+str(statistics.mean(param_vals[i])))
                f.write("Average: "+str(statistics.mean(param_vals[i])) + "\n")
                print("Sample SD: "+str(statistics.stdev(param_vals[i])))
                f.write("Sample SD: "+str(statistics.stdev(param_vals[i])) + "\n")
                print("Min: "+str(min(param_vals[i])))
                f.write("Min: "+str(min(param_vals[i])) + "\n")
                percentiles = np.array([0.1, 1, 2.5, 5, 10, 25, 50, 75, 90, 95, 97.5, 99, 99.9])
                for j in percentiles:
                    print("Percentile " + str(j) + ": " + str(np.percentile(param_vals[i], j)))
                    f.write("Percentile " + str(j) + ": " + str(np.percentile(param_vals[i], j)) + "\n")
                print("Max: "+str(max(param_vals[i])))
                f.write("Max: "+str(max(param_vals[i])) + "\n")
                print("Skewness: "+str(skew(param_vals[i])))
                f.write("Skewness: "+str(skew(param_vals[i])) + "\n")
                print("Kurtosis: "+str(kurtosis(param_vals[i])))
                f.write("Kurtosis: "+str(kurtosis(param_vals[i])) + "\n")
                f.close()
            else:
                newpath=path['path']+'\\'+runName
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                master_path = os.path.dirname(os.path.abspath('final_pdf.py'))
                filePath=master_path+'\\'+'path'+'.json'
                with open(filePath) as fp:
                    path=json.load(fp)
                newpath=path['path']+'\\'+ runName
                print(newpath)
                f = open(newpath+'\\' + runName + " " + sector_name + ".txt", "w")
                print(param_name + ' of ' + sector_name + ' Sector Efficiency')
                f.write(param_name + ' of ' + sector_name + ' Sector Efficiency \n')
                print("Average: "+str(statistics.mean(param_vals[i])))
                f.write("Average: "+str(statistics.mean(param_vals[i])) + "\n")
                print("Sample SD: "+str(statistics.stdev(param_vals[i])))
                f.write("Sample SD: "+str(statistics.stdev(param_vals[i])) + "\n")
                print("Min: "+str(min(param_vals[i])))
                f.write("Min: "+str(min(param_vals[i])) + "\n")
                percentiles = np.array([0.1, 1, 2.5, 5, 10, 25, 50, 75, 90, 95, 97.5, 99, 99.9])
                for j in percentiles:
                    print("Percentile " + str(j) + ": " + str(np.percentile(param_vals[i], j)))
                    f.write("Percentile " + str(j) + ": " + str(np.percentile(param_vals[i], j)) + "\n")
                print("Max: "+str(max(param_vals[i])))
                f.write("Max: "+str(max(param_vals[i])) + "\n")
                print("Skewness: "+str(skew(param_vals[i])))
                f.write("Skewness: "+str(skew(param_vals[i])) + "\n")
                print("Kurtosis: "+str(kurtosis(param_vals[i])))
                f.write("Kurtosis: "+str(kurtosis(param_vals[i])) + "\n")
                f.close()
                  

            
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
