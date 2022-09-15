from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'productInfo', views.ProductInfoViewSet)
router.register(r'product', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('hello_world', views.hello_world),
    path('hello_world2', views.hello_world2),
    path('hello_world_view', views.HelloWorldView.as_view(),
         name='hello_world_view'),
    path('api_test', views.api_test),
]
