from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('<int:id>/', views.product_detail, name='product_detail'),
]