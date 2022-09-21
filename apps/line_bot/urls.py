from django.contrib import admin
from django.urls import path
from . import views  # Add this line

urlpatterns = [
    path('', views.callback),
    path('crawl-stock', views.crawl_stock),
    path('exchage-rate', views.crawl_exchage_rate),
]
