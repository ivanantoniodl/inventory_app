from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('apps.home.urls','home')),
    # Include other app URLs here
]