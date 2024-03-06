from django.urls import path

from . import views

urlpatterns = [
    path("industries/", views.all_industries, name="industries"),
]
