from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import CustomPasswordResetView


urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('user/create/', views.user_create, name="user-create"),
    path('user/edit/<int:id>/', views.user_create, name="user-create"),
    path('user/change-password/', views.change_password, name="change-password"),
    path('user/list/', views.view_users, name="view-users"),
    path('user/info/<int:user_id>/', views.view_user_details, name="user-info"),
    path('user/delete/<int:user_id>/', views.delete_user, name="user-delete"),
    path('user/download/excel/', views.accounts_excel, name="account-excel"),
    path('user/download/csv/', views.accounts_csv, name="account-csv"),
    path('user/download/pdf/', views.accounts_pdf, name="account-pdf"),
    #url paths for password resetting
    path('password_reset/',CustomPasswordResetView.as_view(template_name='account/forgetpassword.html'), name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='account/resetpassword.html'), name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
