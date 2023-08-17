from django.urls import path

from . import views


urlpatterns = [
    path('faq/create/', views.faq_create, name="faq-create"),
    path('faq/display/', views.faq_display, name="faq-display"),
    path('faq/list/', views.faq_list, name="faq-list"),
    path('faq/delete/<int:faq_id>/', views.faq_delete, name="faq-delete"),
    path('faq/edit/<int:faq_id>/', views.faq_edit, name="faq-edit"),
]
