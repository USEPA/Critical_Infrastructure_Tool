
from fpdf import FPDF
import PyPDF2
from PIL import Image
import os
import pandas as pd
import matplotlib.pyplot as plt


def createPdf(ranked_dict, ranked_dict_rt, filename, sensitivity, paramIndexes, paramTypes, n0, nRun, contaminated = False):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_fill_color(204, 255, 204)
    width= 70
    height = 10
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height,"Introduction", ln=1)
    introText1 = "The results below for the {} scenario were produced by the Stochastic Infrastructure".format(filename)
    introText2 = "Remediation Model (SIRM). The SIRM's mechanics are based on the Gillespie Algorithm of stochastically"
    introText3 = "modeling chemical kinetic systems, with adjustments made to suit the modeling of infrastructure remediation"
    introText3b = "after an event that incapacitates infrastructure sectors (e.g. a CBRN event)."
    pdf.cell(width, 5, ln=1)
    introText4 = "The SIRM examines the interactions of 9 different infrastructure sectors: Water, Energy, Transportation,"
    introText5 = "Communication, Government, Food/Agriculture, Emergency Services, Waste Management and Healthcare."
    introText6a = "Based on the initial operating efficiency after the event, the model calculates an estimated time"
    introText6b = "for recovery for each sector, averaged from a user-defined number of model runs ({}).".format(str(nRun))
    pdf.set_font('Times','', 12)
    pdf.cell(width, 5,introText1, ln=1)
    pdf.cell(width, 5,introText2, ln=1)
    pdf.cell(width, 5,introText3, ln=1)
    pdf.cell(width, 5,introText3b, ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.cell(width, 5,introText4, ln=1)
    pdf.cell(width, 5,introText5, ln=1)
    pdf.cell(width, 5,introText6a, ln=1)
    pdf.cell(width, 5,introText6b, ln=1)
    pdf.cell(width, 5, ln=1)

    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height,"Initial Inputs", ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.set_font('Times','', 12)
    introText7 = "The initial set of infrastructure operating efficiencies input into the tool are displayed below:"
    pdf.cell(width, 5,introText7, ln=1)
    pdf.cell(width, 5, ln=1)
    sector_list = ["Water", "Energy", "Transportation", "Communications", "Government", "Food & Agriculture",
                   "Emergency Services", "Waste Management", "Healthcare"]
    data = ["Infrastructure Sector", "Initial Efficiency (%)"]
    pdf.cell(width, height, str(data[0]), border=1, fill = True)
    pdf.cell(width, height, str(data[1]), border=1, ln=1, fill = True)
    for i in range(len(n0)):
        pdf.cell(width, height, str(sector_list[i]), border=1)
        pdf.cell(width, height, str(n0[i]), border=1, ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height,"Results", ln=1)
    pdf.cell(width, 5, ln=1)
    pdf.set_font('Times','', 12)
    pdf.cell(width, 5, 'The SIRM tool outputs the following set of result, which are provided in this report: \n', ln=1)
    pdf.cell(width, 5, '1) The suggested prioritization of sector remediation\n', ln=1)
    pdf.cell(width, 5, '2) Various charts of the results\n', ln=1)
    pdf.cell(width, 5, '3) Requested sensitivity analyses\n', ln=1)
    pdf.cell(width, 5, '4) (optional) If it is a contamination event, the number and types of contaminated buildings will be listed as well \n', ln=1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, 'Suggested sector prioritization based on strength of infrastructure connections: \n', ln=1)
    i = 1
    pdf.set_font('Times', '', 12)
    data = ["Infrastructure Sector", "Connection Strength"]
    pdf.cell(width, height, str(data[0]), border=1, fill = True)
    pdf.cell(width, height, str(data[1]), border=1, ln=1, fill = True)
    for key, value in ranked_dict:
        data = [key, str(round(float(value), 2))]
        pdf.cell(width, height, str(data[0]), border=1)
        pdf.cell(width, height, str(data[1]), border=1, ln=1)
        i += 1
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, 'Suggested sector prioritization based on median recovery time: \n', ln=1)
    i = 1
    pdf.set_font('Times', '', 12)
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
    pdf.image(name, w=150)
    #pdf.cell(width, height, "Sector Operating Efficiency over Time", ln=1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height, "Requested Charts", ln=1)
    pdf.cell(width, height, ln=1)
    if len(paramIndexes) < 1:
        pdf.cell(width, height, "No charts were requested by the SIRM tool user", ln=1)
    for i in range(len(paramIndexes)):
        sector_name = getSector(paramIndexes[i])
        graph = "Images/" + filename + " " + sector_name
        name = graph + ".png"
        
        pdf.image(name, w=150)
    pdf.cell(width, height, "Requested Sensitivity Analyses", ln=1)
    if len(sensitivity) < 1:
        pdf.set_font('Times', '', 12)
        pdf.cell(width, height, "No sensitivity analyses were requested by the user", ln=1)
    pdf.set_font('Times', 'B', 12)
    for g in range(len(sensitivity)):
        graph = "Sensitivity Images/" + getSector(sensitivity[g]) + " Sensitivity.png"
        pdf.image(graph, w=150)
    if contaminated:
        pdf.set_font('Times', 'B', 12)
        pdf.cell(width, height, "The number and type of contaminated buildings :", ln=1)
        pdf.set_font('Times', '', 12)
        pdf = getInfrastructureList("Contaminated//", pdf, width, 5)
    disclaimer1 = "Disclaimer: The results produced here are estimates and created through the use of the SIRM model."
    disclaimer2 = "Point of Contact: Timothy Boe, EPA, Timothy.Boe@epa.gov"
    pdf.cell(width, height,disclaimer1, ln=1)
    pdf.cell(width, height,disclaimer2, ln=1)
    pdf.output('Results/' + filename + "_Report.pdf", 'F')

def getInfrastructureList(location, pdf, width, height):
    data ={"Building Type": [], "Number of Buildings": []} 
    tempresults = pd.DataFrame(data)
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
                new_row = {"Building Type": str(building_type).capitalize(), "Number of Buildings":len(results)}
                tempresults = tempresults.append(new_row, ignore_index=True)
            #print(tempresults)
            #print(new_row)
    #plt.rcParams.update({'font.size': 12})
    fig1, ax1 = plt.subplots()
    #print(tempresults)
    patches, texts, autotexts = ax1.pie(tempresults["Number of Buildings"], labels=tempresults["Building Type"],
            autopct = autopct_format(tempresults["Number of Buildings"]), startangle=90, pctdistance=0.85, labeldistance=1.2)
    ax1.axis('equal')
    plt.style.use('ggplot')
    #p = ggplot(tempresults, aes(x='Number of Buildings', fill = 'Building Type'))+ geom_bar() + coord_polar(theta = "y")
    plt.savefig(location + "//PieChart.png", dpi=60, bbox_inches = "tight")
    pdf.image(location + "//PieChart.png")
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
    
