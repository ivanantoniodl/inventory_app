from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('apps.home.urls','home')),
    path('productos/', include('apps.productos.urls','productos')),
    path('lugares/', include('apps.lugares.urls','lugares')),
    path('compras/', include('apps.compras.urls', 'compras')),
]