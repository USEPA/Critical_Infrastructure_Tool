
from fpdf import FPDF
import PyPDF2
from PIL import Image
import os
import pandas as pd
import matplotlib.pyplot as plt
from plotnine import *
from matplotlib import rcParams

#Root = os.path.abspath(os.path.dirname(__file__))


def createPdf(ranked_dict, ranked_dict_rt, filename, sensitivity, paramIndexes, paramTypes, n0, nRun, timeSpan, contamination, contaminated = False):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_fill_color(204, 255, 204)
    width= 70
    height = 10
    pdf.set_font('Times', 'B', 16)
    pdf.cell(width, 5,filename + " SIRM Results", ln=1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height,"Introduction", ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.set_font('Times','', 12)
    introTextBlurb = "Large-scale chemical, biological, radiological, and nuclear (CBRN) incidents, whether a product of terrorism,"
    introTextBlurb2 = "war, or accidents, have the potential to damage core infrastructure assets."
    introTextBlurb3 = "In these situations, not only are directly affected areas not able to operate, but operations in other infrastructure "
    introTextBlurb4 = "sectors may not be able to operate without the services of the affected assets."
    pdf.cell(width, 5,introTextBlurb, ln=1)
    pdf.cell(width, 5,introTextBlurb2, ln=1)
    pdf.cell(width, 5,introTextBlurb3, ln=1)
    pdf.cell(width, 5,introTextBlurb4, ln=1)
    pdf.cell(width, 5, ln=1)
    introTextPt2 = "The Stochastic Infrastructure Remediation Model (SIRM) tool allows for a series of interconnected"
    introTextPt3 = "infrastructure sectors to be modeled and considers the realistic variability of the impact of a CBRN event."
    pdf.cell(width, 5,introTextPt2, ln=1)
    pdf.cell(width, 5,introTextPt3, ln=1)
    
    introText1 = "The results below for the {} scenario were produced by a Python tool that performs the SIRM calculations. ".format(filename)
    introText2 = "The SIRM's mechanics are based on the Gillespie Algorithm of stochastically modeling chemical kinetic systems, "
    introText3 = "with adjustments made to suit the modeling of infrastructure remediation after an event that incapacitates"
    introText3b = "infrastructure sectors (e.g. a CBRN event)."
    introText4 = "The SIRM examines the interactions of 9 different infrastructure sectors: Water, Energy, Transportation,"
    introText5 = "Communication, Government, Food/Agriculture, Emergency Services, Waste Management and Healthcare."
    introText6a = "Based on the initial operating efficiency after the event, the model calculates an estimated time"
    introText6b = "for recovery for each sector, averaged from a user-defined number of model runs ({}).".format(str(nRun))
    pdf.set_font('Times','', 12)
    pdf.cell(width, 5,introText2, ln=1)
    pdf.cell(width, 5,introText3, ln=1)
    pdf.cell(width, 5,introText3b, ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.cell(width, 5,introText4, ln=1)
    pdf.cell(width, 5,introText5, ln=1)
    pdf.cell(width, 5,introText6a, ln=1)
    pdf.cell(width, 5,introText6b, ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.cell(width, 5,introText1, ln=1)
    pdf.cell(width, height, "A map of the scenario is depicted below", ln=1)
    pdf.image("Results//Mapping.png", w=180)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height,"Initial Inputs", ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.set_font('Times','', 12)
    introText7 = "The initial set of post-event infrastructure operating efficiencies input in the tool are displayed below:"
    pdf.cell(width, 5,introText7, ln=1)
    pdf.cell(width, 5, ln=1)
    sector_list = ["Water", "Energy", "Transportation", "Communications", "Government", "Food & Agriculture",
                   "Emergency Services", "Waste Management", "Healthcare"]
    data = ["Infrastructure Sector", "Initial Efficiency (%)", "Initial Contamination"]
    pdf.cell(60, height, str(data[0]), border=1, fill = True)
    pdf.cell(60, height, str(data[1]), border=1, fill = True)
    pdf.cell(60, height, str(data[2]), border=1, ln=1, fill = True)
    for i in range(len(n0)):
        pdf.cell(60, height, str(sector_list[i]), border=1)
        pdf.cell(60, height, str(n0[i]), border=1)
        if len(contamination) > 0:
            pdf.cell(60, height, str(round((100-contamination[i]),1)), border=1, ln=1)
        else:
            pdf.cell(60, height, str(0), border=1, ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.set_font('Times', 'B', 12)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, "The number and type of affected buildings/infrastructure :", ln=1)
    pdf.set_font('Times', '', 12)
    pdf.cell(width, 5, "Based on the map information, the tool produces a list of affected buildings/infrastructure. ", ln=1)
    pdf.cell(width, 5,"Some are affected by outages, while others may require decontamination.", ln=1)         
    pdf.set_font('Times', '', 12)
    pdf = getInfrastructureList("Contaminated//", pdf, width, 5, "Affected//", contaminated)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height,"Results", ln=1)
    pdf.cell(width, 2, ln=1)
    pdf.set_font('Times','', 12)
    pdf.cell(width, 5, 'The SIRM tool outputs the following set of results, which are provided in this report: \n', ln=1)
    pdf.cell(width, 5, '1) The suggested prioritization of sector remediation\n', ln=1)
    pdf.cell(width, 5, '2) Various charts of the results\n', ln=1)
    pdf.cell(width, 5, '3) Requested sensitivity analyses\n', ln=1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, 'Estimated Infrastructure Sector Prioritization Based on Strength of Infrastructure Connections: \n', ln=1)
    i = 1
    pdf.set_font('Times', '', 12)
    prior1 = "The first prioritization is based on how tightly linked an infrastructure is to other infrastructure sectors."
    prior2 = "The higher the connection strength, the more other infrastructure sectors are dependant on that infrastructure."
    prior3 = "Infrastructures with more dependancies will be prioritized in this ranking."
    
    data = ["Infrastructure Sector", "Connection Strength"]
    pdf.cell(width, 5, prior1,ln=1)
    pdf.cell(width, 5, prior2,ln=1)
    pdf.cell(width, 5, prior3,ln=1)
    pdf.cell(width, height, str(data[0]), border=1,fill = True)
    pdf.cell(width, height, str(data[1]), border=1, ln=1, fill = True)
    for key, value in ranked_dict:
        data = [key, str(round(float(value), 2))]
        pdf.cell(width, height, str(data[0]), border=1)
        pdf.cell(width, height, str(data[1]), border=1, ln=1)
        i += 1
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, 'Estimated Infrastructure Prioritization Based on Median Recovery Time: \n', ln=1)
    i = 1
    pdf.set_font('Times', '', 12)
    prior1 = "The second prioritization is based to the average calculated recovery time in days for each sector."
    prior2 = "Infrastructures with longer average recovery times will be prioritized in this ranking."
    pdf.cell(width, 5, prior1,ln=1)
    pdf.cell(width, 5, prior2, ln=1)
    
    data = ["Infrastructure Sector", "Recovery Time (days)"]
    pdf.cell(width, height, str(data[0]), border=1, fill = True)
    pdf.cell(width, height, str(data[1]), border=1, ln=1, fill = True)
    for key, value in ranked_dict_rt:
        data = [key, str(round(float(value), 2))]
        pdf.cell(width, height, str(data[0]), border=1)
        pdf.cell(width, height, str(data[1]), border=1, ln=1)
        i += 1
    pdf.cell(width, height, ln=1)   
    #adding sensitivity
    graph = "Images/" + filename
    name = graph + ".png"
    
    #pdf.cell(width, height, "Sector Operating Efficiency over Time", ln=1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, "Graphical Output and Interpretation", ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.set_font('Times', '', 12)
    prior1 = "The graphs below represent requested outputs for various infrastructure sectors. The first graph charts the "
    prior2 = "efficiency of each sector over time."
    pdf.cell(width, 5, prior1,ln=1)
    pdf.cell(width, 5, prior2,ln=1)
    pdf.image(name, w=150)
    pdf.cell(width, 5, "The following charts were also requested by the user of the tool.",ln=1)
    if len(paramIndexes) < 1:
        pdf.cell(width, height, "No charts were requested by the SIRM tool user", ln=1)
    for i in range(len(paramIndexes)):
        sector_name = getSector(paramIndexes[i])
        graph = "Images/" + filename + " " + sector_name
        name = graph + ".png"
        
        pdf.image(name, w=150)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, "Requested Sensitivity Analyses", ln=1)
    pdf.set_font('Times', '', 12)
    pdf.cell(width, 5, "The user also has the option of running sensitivity analyses on various inputs in the tool. The results of the requested", ln=1)
    pdf.cell(width, 5, "sensitivity analyses are below.", ln=1)
    pdf.cell(width, 5, ln=1)
    if len(sensitivity) < 1:
        pdf.set_font('Times', '', 12)
        pdf.cell(width, height, "No sensitivity analyses were requested by the user", ln=1)
    pdf.set_font('Times', 'B', 12)
    for g in range(len(sensitivity)):
        graph = "Sensitivity Images/" + getSector(sensitivity[g]) + " Sensitivity.png"
        pdf.image(graph, w=150)
    disclaimer1 = "Disclaimer: The results produced here are estimates and created through the use of the SIRM model."
    disclaimer1b = "the tool doesn’t account for auxiliary infrastructure such as power lines, water pipes, etc."
    disclamer1c = "that may impact operations/recovery."
    disclaimer2 = "Point of Contact: Timothy Boe, EPA, Timothy.Boe@epa.gov"
    pdf.cell(width, height,disclaimer1, ln=1)
    pdf.cell(width, height,disclaimer2, ln=1)
    pdf.output('Results/' + filename + "_Report.pdf", 'F')

def getInfrastructureList(location, pdf, width, height, location2, contaminated, location3 = "Overall//"):
    data ={"Building Type": [], "Number of Contaminated buildings/infrastructure": []}
    dataAffected ={"Building Type": [], "Number of Affected buildings/infrastructure": []}
    dataOverall = {"Building Type": [], "Total number of buildings/infrastructure": []}
    tempresults = pd.DataFrame(data)
    tempresults2 = pd.DataFrame(dataAffected)
    tempresults3 = pd.DataFrame(dataOverall)
    pdf.cell(width, 5,ln=1)
    pdf.cell(width, height, "Number of buildings/infrastructure requiring decontamination:", ln=1)
    if contaminated:
        for filename in os.listdir(location):
            if filename.endswith(".csv") and "contaminated" in filename:
                filenames = filename.split("_c")
                building_type = filenames[0]
                building_type = building_type.split("_")
                building_type = ' '.join(building_type)
                results = pd.read_csv(os.path.join(location, filename))
                text = "{} : {}".format(str(building_type).capitalize(),
                                        str(len(results)))
                pdf.cell(width, height, text, ln=1)
                if len(results)>0:
                    new_row = {"Building Type": str(building_type).capitalize(), "Number of Contaminated buildings/infrastructure":len(results)}
                    tempresults = tempresults.append(new_row, ignore_index=True)
    pdf.cell(width, height, ln=1)
    pdf.cell(width, height, "Number of affected buildings/infrastructure:", ln=1)
    for filename in os.listdir(location2):
        if filename.endswith(".csv") and "contaminated" in filename:
            filenames = filename.split("_c")
            building_type = filenames[0]
            building_type = building_type.split("_")
            building_type = ' '.join(building_type)
            results = pd.read_csv(os.path.join(location2, filename))
            text = "{} : {}".format(str(building_type).capitalize(),
                                    str(len(results)))
            pdf.cell(width, height, text, ln=1)
            if len(results)>0:
                new_row = {"Building Type": str(building_type).capitalize(), "Number of Affected buildings/infrastructure":len(results)}
                tempresults2 = tempresults2.append(new_row, ignore_index=True)
    pdf.cell(width, height, ln=1)
    pdf.cell(width, height, "Total buildings/infrastructure in area:", ln=1)
    for filename in os.listdir(location3):
        if filename.endswith(".csv") and "contaminated" in filename:
            filenames = filename.split("_c")
            building_type = filenames[0]
            building_type = building_type.split("_")
            building_type = ' '.join(building_type)
            results = pd.read_csv(os.path.join(location3, filename))
            text = "{} : {}".format(str(building_type).capitalize(),
                                    str(len(results)))
            pdf.cell(width, height, text, ln=1)
            if len(results)>0:
                new_row = {"Building Type": str(building_type).capitalize(), "Total number of buildings/infrastructure":len(results)}
                tempresults3 = tempresults3.append(new_row, ignore_index=True)
    fig1, ax1 = plt.subplots()
    #print(tempresults)
    #patches, texts, autotexts = ax1.pie(tempresults["Number of Buildings"], labels=tempresults["Building Type"],
            #autopct = autopct_format(tempresults["Number of Buildings"]), startangle=90, pctdistance=0.85, labeldistance=1.2)
    ax1.axis('equal')
    #plt.style.use('ggplot')
    if contaminated and len(tempresults) > 0:
        result = pd.merge(tempresults, tempresults2, on="Building Type")
        finalresult = pd.merge(tempresults3, result, on="Building Type")
    else:
        finalresult = pd.merge(tempresults3, tempresults2, on="Building Type")
    #p = ggplot(finalresult, aes(x='Building Type', y='Number of Contaminated Buildings',fill = 'Building Type'))+ geom_col() + geom_col(aes(y='Number of Affected Buildings',x = 'Building Type', fill = 'Building Type')) + geom_col(aes(y='Number of Buildings', x = 'Building Type', fill = 'Building Type'))
    
    font = {'family' : 'normal',
        'size'   : 10}
    plt.rc('font', **font)
    
    p = finalresult.groupby('Building Type').mean().plot(kind='bar')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    plt.xticks(rotation = -45, fontsize=8)
    plt.tight_layout()
    rcParams.update({'figure.autolayout': True})
    p.get_figure().savefig('ColumnChart.png')
    pdf.image(dir_path+"\\ColumnChart.png", w=200)
    return pdf

    
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_format

def getSector(index):
    if index == 0:
        return "Water"
    elif index == 1:
        return "Energy"
    elif index == 2:
        return "Transportation"
    elif index == 3:
        return "Communication"
    elif index == 4:
        return "Government"
    elif index == 5:
        return "Food"
    elif index == 6:
        return "Emergency Services"
    elif index == 7:
        return "Waste"
    else:
        return "Healthcare"
    
