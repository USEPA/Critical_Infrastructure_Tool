
from fpdf import FPDF
import PyPDF2
from PIL import Image
import os
import pandas as pd

def createPdf(ranked_dict, ranked_dict_rt, filename, sensitivity, paramIndexes, paramTypes, contaminated = False):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times', 'B', 12)
    pdf.set_fill_color(204, 255, 204)
    width= 70
    height = 10
    pdf.cell(width, height, 'The results are displayed below \n', ln=1)
    pdf.cell(width, height, 'Rank by strength of infrastructure connections: \n', ln=1)
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
    pdf.cell(width, height, 'Rank by median recovery time: \n', ln=1)
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
        pdf = getInfrastructureList("Results//", pdf, width, height)
    #adding sensitivity
    graph = "Images/" + filename
    name = graph + ".png"
    pdf.image(name, w=150)
    for i in range(len(paramIndexes)):
        sector_name = getSector(paramIndexes[i])
        graph = "Images/" + filename + " " + sector_name
        name = graph + ".png"
        pdf.image(name, w=150)
    for g in range(len(sensitivity)):
        graph = "Sensitivity Images/" + getSector(sensitivity[g]) + " Sensitivity.png"
        pdf.image(graph, w=150)
        
    pdf.output('Results/' + filename + "_Report.pdf", 'F')

def getInfrastructureList(location, pdf, width, height):
    for filename in os.listdir(location):
        if filename.endswith(".csv") and "contaminated" in filename:
            filenames = filename.split("_")
            building_type = filenames[0]
            results = pd.read_csv(os.path.join(location, filename))
            text = "{} {} buildings were contaminated".format(str(len(results)), str(building_type).capitalize())
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
    
