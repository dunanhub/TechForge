from django.urls import path
from .views import add_to_cart, view_cart, clear_cart

app_name = 'orders'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('view-cart/', view_cart, name='view_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
]