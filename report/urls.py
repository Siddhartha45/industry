from django.urls import path

from . import views


urlpatterns = [
    path('report/', views.report_problem, name="report"),
    path('report/list/', views.report_list, name="report-list"),
    path('report/show/<int:report_id>/', views.report_show, name="report-show"),
    path('report/delete/<int:report_id>/', views.report_delete, name="report-delete"),
    #url path for import excel files into database
    path('file/', views.import_file, name="file"),
]
