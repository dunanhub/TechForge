from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('<int:category_id>/', views.subcategory_by_category, name='subcategory_by_category'),
    path('<int:category_id>/<int:subcategory_id>/', views.product_list, name='product_list'),
    path('<int:category_id>/<int:subcategory_id>/<int:product_id>/', views.product_detail, name='product_detail'),
]
