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