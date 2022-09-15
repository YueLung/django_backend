from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trial/', include('apps.trial.urls')),
    path('line-bot/', include('apps.line_bot.urls')),
]
