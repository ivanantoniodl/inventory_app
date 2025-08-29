from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('apps.home.urls','home')),
    path('products/', include('apps.productos.urls','products')),
    # Include other app URLs here
]