from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('adminDashboard.urls')),
    path('auth/', include('auth_app.urls')),
    path('', include("shop.urls")),
    path('accounts/', include('allauth.urls')),
]