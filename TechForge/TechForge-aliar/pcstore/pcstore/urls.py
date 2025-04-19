from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('shop.urls')),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    path('orders/', include('orders.urls', namespace='orders')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)