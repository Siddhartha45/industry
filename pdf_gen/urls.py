from django.urls import path
from . import views
urlpatterns = [
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate/', views.industry_pdf, name="industrypdf"),
    path('pdf/', views.report_pdf, name="report-pdf"),
    #path('generate-pdfgen/', views.generate_pdfgen),
    #path('generate-pdfkit/', views.generate_pdfkit),
    #path('generate-pdfkit/', views.generate_print),
]