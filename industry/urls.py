from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home, name="home"),
    path('industry/add/',views.add_industry, name="add-industry"),
    path('industry/edit/<int:industry_id>/', views.edit_industry, name="edit-industry"),
    path('industry/delete/<int:industry_id>/', views.delete_industry, name="industry-delete"),
    path('industry/profile/<int:industry_id>/', views.view_industry_profile, name="industry-profile"),
    path('industry/list/', views.industry_list, name="industry-list"),
    path('industry/search/', views.search_industry, name="search-industry"),
    path('industry/download/excel/', views.industry_excel, name="download-excel"),
    path('industry/download/csv/', views.industry_csv, name="download-csv"),
    path('industry/download/pdf/', views.download_pdf, name="download-pdf"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
