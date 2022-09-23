from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trial/', include('apps.trial.urls')),
    path('line/', include('apps.line.urls')),
]
