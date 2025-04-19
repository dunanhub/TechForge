from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products/', views.products, name='products'),
    path('categories/', views.categories_view, name='categories'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
]