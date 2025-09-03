from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('apps.home.urls','home')),
    path('productos/', include('apps.productos.urls','productos')),
    # Include other app URLs here
]