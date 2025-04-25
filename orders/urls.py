from django.urls import path
from .views import add_to_cart, remove_from_cart, update_quantity, view_cart, clear_cart

app_name = 'orders'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-quantity/<int:item_id>/<str:action>/', update_quantity, name='update_quantity'),
    path('view-cart/', view_cart, name='view_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
]