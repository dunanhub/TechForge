from django.shortcuts import redirect
from django.urls import path
from . import views

# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('check_activation_status/<path:email>/', views.check_activation_status, name='check_activation_status'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth_app/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth_app/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth_app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth_app/password_reset_complete.html'), name='password_reset_complete'),
]