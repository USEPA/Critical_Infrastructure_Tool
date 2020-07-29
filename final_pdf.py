
from fpdf import FPDF

def createPdf(ranked_dict, ranked_dict_rtm, filename):
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
    pdf.output('Results/Report.pdf', 'F')
