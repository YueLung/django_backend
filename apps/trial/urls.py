from django.urls import path
from . import views

urlpatterns = [
      path('hello_world', views.hello_world),
      path('hello_world2', views.hello_world2),
      path('api_test', views.api_test),   
]