
from fpdf import FPDF
import PyPDF2
from PIL import Image
import os
import pandas as pd

def createPdf(ranked_dict, ranked_dict_rt, filename, sensitivity, paramIndexes, paramTypes, contaminated = False):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_fill_color(204, 255, 204)
    width= 70
    height = 10
    pdf.set_font('Times', 'B', 12)
    pdf.cell(width, height,"Introduction", ln=1)
    introText1 = "The results below for the pre-defined scenario were produced by the Stochastic Infrastructure"
    introText2 = "Remediation Model (SIRM). The SIRM's mechanics are based on the Gillespie Algorithm of stochastically"
    introText3 = "modeling chemical kinetic systems, with changes made to adapt to infrastructure modeling."
    pdf.set_font('Times','', 12)
    pdf.cell(width, height,introText1, ln=1)
    pdf.cell(width, height,introText2, ln=1)
    pdf.cell(width, height,introText3, ln=1)
    
    pdf.cell(width, height, 'The suggested prioritization of sector remediation is tabulated below \n', ln=1)
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

    if contaminated:
        pdf.set_font('Times', 'B', 12)
        pdf.cell(width, height, "The number and type of contaminated buildings :", ln=1)
        pdf.set_font('Times', '', 12)
        pdf = getInfrastructureList("Contaminated//", pdf, width, height)
    #adding sensitivity
    graph = "Images/" + filename
    name = graph + ".png"
    pdf.image(name, w=150)
    for i in range(len(paramIndexes)):
        sector_name = getSector(paramIndexes[i])
        graph = "Images/" + filename + " " + sector_name
        name = graph + ".png"
        pdf.cell(width, height, "Sector Operating Efficiency over Time", ln=1)
        pdf.image(name, w=150)
    for g in range(len(sensitivity)):
        pdf.cell(width, height, "Sensitivity Graphs", ln=1)
        graph = "Sensitivity Images/" + getSector(sensitivity[g]) + " Sensitivity.png"
        pdf.image(graph, w=150)

    disclaimer1 = "The results produced here are estimates and created through the use of the SIRM model."
    disclaimer2 = "Point of Contact: Timothy Boe, EPA, Timothy.Boe@epa.gov"
    pdf.cell(width, height,disclaimer1, ln=1)
    pdf.cell(width, height,disclaimer2, ln=1)
    pdf.output('Results/' + filename + "_Report.pdf", 'F')

def getInfrastructureList(location, pdf, width, height):
    for filename in os.listdir(location):
        if filename.endswith(".csv") and "contaminated" in filename:
            filenames = filename.split("_c")
            building_type = filenames[0]
            building_type = building_type.split("_")
            building_type = ' '.join(building_type)
            results = pd.read_csv(os.path.join(location, filename))
            text = "{} : {}".format(str(building_type).capitalize(), str(len(results)))
            pdf.cell(width, height, text, ln=1)
    return pdf    

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
    
