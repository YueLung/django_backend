from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view

from apps.trial.serializers import ProductInfoSerializer, ProductSerializer
from .models import Product, ProductCategory


def hello_world(request):
    return HttpResponse("Hello World!")


def hello_world2(request):
    return render(request, 'hello_world.html', {
        'current_time': str(datetime.now()),
    })


class HelloWorldView(generics.GenericAPIView):
    def get(self, reques):
        return Response(data={"message": "hello world"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_test(request, *args, **kwargs):
    return Response({"data": "api test OK from django backend"}, status=200)


class ProductInfoViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductInfoSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
