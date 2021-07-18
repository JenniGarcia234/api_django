from enum import unique
from rest_framework import serializers
from .models import Product, Category 


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name','description', 'sku', 'buyPrice', 'quantity', 'category']
     

class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'active','description', 'sku', 'buyPrice', 'quantity', 'category']


class CategoryListSerializer(serializers.ModelSerializer):

     class Meta:
         model = Category
         fields = ['id', 'title']