from django.urls import path

from . import views


urlpatterns = [
    path('industry-without-gis/list/', views.without_gis_industry_list, name="industry_without_gis_list"),
    path('industry-ajax-search-without-gis/', views.AjaxSearchWithousGis, name="AjaxSearchWithoutGis"),
    path('industry-without-gis/session-reset/', views.session_delete, name="session_reset_without_gis"),
    path('industry-without-gis/profile/<int:industry_id>/', views.view_industry_profile_without_gis, name="industry_profile_without_gis"),
    path('industry-without-gis/delete/<int:industry_id>/', views.delete_industry_without_gis, name="industry_delete_without_gis"),
    path('industry-without-gis/edit/<int:industry_id>/', views.edit_industry_without_gis, name="edit_industry_without_gis"),
    path('industry-without-gis/download/excel/', views.without_gis_industry_excel, name="without_gis_excel"),
    path('industry-without-gis/download/csv/', views.without_gis_industry_csv, name="without_gis_csv"),
    path('industry-without-gis-profile/download/pdf/<int:industry_id>/', views.industry_without_gis_profile_pdf, name="industry_without_gis_profile_pdf"),
    path('industry-without-gis/download/pdf/', views.without_gis_download_pdf, name="industry_without_gis_download_pdf"), 
    
    # path('translation_settings/', views.translation_settings, name='translation_settings'),
]
