from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from reportlab.pdfgen import canvas
from django.utils.translation import activate, gettext as _
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from industry.models import Industry
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


def generate_pdf(request):
    # Create a HttpResponse object with PDF mimetype
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="example.pdf"'
    
    # Register the font with ReportLab
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(BASE_DIR, 'fonts', 'FreeSans.ttf')
    pdfmetrics.registerFont(TTFont('FreeSans', font_path))
    
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)
    # Specify the font for rendering Hindi text
    p.setFont("FreeSans", 12)  # Font name should match the registered font name

    p.drawString(100, 750, 'ss उर्जामूलक')
    p.drawString(50, 70, 'उर्जामूलक')
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


def industry_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    
    # Register the custom font with ReportLab
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(BASE_DIR, 'fonts', 'NotoSansD.ttf')
    pdfmetrics.registerFont(TTFont('NotoSansD', font_path, 'UTF-8'))
    
    textob.setFont("NotoSansD", 12)  # Use the registered font name
    
    lines = [
        "pdf",
        "report",
        "सिद्धार्थ थापा",
    ]
    
    for line in lines:
        textob.textLine(line)
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    
    return FileResponse(buf, filename='industry.pdf')


#fpdf
from fpdf import FPDF
from io import BytesIO
def report_pdf(request):
    pdf = FPDF('P', 'mm', 'Letter')
    pdf.add_page()
    
    pdf.add_font(fname='fonts/NotoSansD.ttf')
    pdf.set_font('NotoSansD', size=16)
    
    pdf.cell(40, 10, 'Hello सिद्धार्थ थापा')
    #pdf.output('report.pdf')
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    return response


# from pdfgen import Document
# def generate_pdfgen(request):
#     # Create a new PDF document
#     doc = Document()
    
#     # Add content to the PDF
#     doc.add_text("Hello, World!")
    
#     # Generate the PDF content
#     pdf_content = doc.render()
    
#     # Create a response object with the PDF content
#     response = HttpResponse(pdf_content, content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="example.pdf"'
    
#     return response


# import pdfkit
# def generate_pdfkit(request):
#     text_content = "Hello, World!"
#     pdf_data = pdfkit.from_string(text_content, False)
    
#     response = HttpResponse(pdf_data, content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="example.pdf"'
    
#     return response



# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile

# def generate_print(request):
    
#     response = HttpResponse(content_type='application/pdf')
#     response ['Content-Disposition'] = 'filename=industry.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'
    
#     html_string = render_to_string('industry/print_pdf.html', {'industry': [], 'total': 0})
#     html = HTML(string=html_string)
    
#     result = html.write_pdf()
    
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
        
#         output=open(output.name, 'rb')
#         response.write(output.read())
        
#     return response