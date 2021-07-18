from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework import generics, permissions 
from products.models import Product, Category
from .serializers import ProductListSerializer, ProductDetailSerializer, CategoryListSerializer
from rest_framework import status

# Create your views here.

class ProductsList(ListCreateAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    
    def get_queryset(self):

        try:
            product = Product.objects.all().filter(active=True)
        except Product.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return product
    # Create una producto
    def post(self, request):
        data = request.data
        sku1 = str(data['sku'])
        serializer = ProductListSerializer(data=request.data)
        sku_exists=Product.objects.get(sku=sku1)
        result=str(sku_exists.sku)
        if serializer.is_valid():
            if result!=sku1:
                serializer.save(activate=True, sku=sku1)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'The product SKU alredy exists, please check the SKU'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer

    def get_queryset(self, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return product

    # Get a product
    def get(self, request, id):

        product = self.get_queryset(id)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a product
    def put(self, request, id):
        
        product= self.get_queryset(id)
        product1= Product.objects.get(id=id)
        serializer = ProductDetailSerializer(product, data=request.data)
        data = request.data
        sku1 = str(data['sku'])
        sku_exists=Product.objects.get(sku=sku1)
        result=str(sku_exists.sku)
        if serializer.is_valid():
            if product1.id== sku_exists.id:
                serializer.save(sku=sku1)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif product1.id== sku_exists.id:
                return Response({'The product SKU alredy exists, please check the SKU'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete un product
    def delete(self, request, id):

        product = self.get_queryset(id)
        product.delete()
        content = {
                'status': 'NO CONTENT'
            }
        return Response(content, status=status.HTTP_204_NO_CONTENT)


class CategoryListApiView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Category.objects.filter(active=True)


class ProductListApiAuthView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Product.objects.all()