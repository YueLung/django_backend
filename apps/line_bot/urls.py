from django.contrib import admin
from django.urls import path
from . import views  # Add this line

urlpatterns = [
    path('', views.callback),
]
