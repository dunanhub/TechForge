from django.urls import path, include
from . import views
from .views import google_auth_callback

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    # path("accounts/", include("allauth.urls")),

    path('', views.sign_in, name='sign_in'),
    path('sign-out', views.sign_out, name='sign_out'),
    path("auth-receiver/", google_auth_callback, name="auth_receiver"),
]
