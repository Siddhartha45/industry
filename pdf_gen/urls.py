from django.urls import path
from . import views
urlpatterns = [
    path('generate/', views.industry_pdf, name="industrypdf"),
]