from rest_framework import serializers
from .models import Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        # fields = ['id', 'name', 'price', 'photo']
        fields = '__all__'
        extra_kwargs = {'category': {'required': False},
                        'name': {'required': False},
                        'price': {'required': False}}


class ProductInfoSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'products']
        # fields = '__all__'
