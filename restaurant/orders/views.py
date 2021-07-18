from django.db import models
from django.utils.translation import activate
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order
from .models import OrderItem
from products.models import Product
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


# Create your views here.

class OrderList(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(activate=True)

    # Create an new order 
    def post(self, request):
       
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(activate=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###Order Crud
class OrderDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self, id):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return order

    # Get an order
    def get(self, request, id):

        order= self.get_queryset(id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a order
    def put(self, request, id):
        
        order= self.get_queryset(id)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
          
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete and order
    def delete(self, request, id):

        order = self.get_queryset(id)
        order.delete()
        content = {
                'status': 'NO CONTENT'
            }
        return Response(content, status=status.HTTP_204_NO_CONTENT)

        




#View Get and post Orderitem por parametro idOrder
class OrderItemL(ListCreateAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    
    def get_queryset(self):
        order_id=self.kwargs['order_id']
        return self.queryset.filter(order=order_id)
        
    def post(self, request,*args, **kwargs,):
            data = request.data
            product = data['product']
            quantity_r=int(data['quantity'])
            order_id= Order.objects.get(id=self.kwargs['order_id'])
            serializer = OrderItemSerializer(data=request.data)
            product_exist=Product.objects.get(id=product)
            result=int(product_exist.quantity)
            if serializer.is_valid():
                 if result>=quantity_r:
                
                    serializer.save(activate=True, order=order_id)
                    product_exist.quantity= product_exist.quantity-quantity_r
                    product_exist.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                 else:
                     return Response({'The product is out of stock'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


class OrderItemDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self, id):
        try:
            orderitem = OrderItem.objects.get(id=id)
        except OrderItem.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return orderitem

    # Get a irderitem
    def get(self, request, id):

        orderitem = self.get_queryset(id)
        serializer = OrderItemSerializer(orderitem)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a orderitem
    def put(self, request, id):
        
        orderitem= self.get_queryset(id)
        serializer = OrderItemSerializer(orderitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
          
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete un product
    def delete(self, request, id):

        orderitem = self.get_queryset(id)
        orderitem.delete()
        content = {
                'status': 'NO CONTENT'
            }
        return Response(content, status=status.HTTP_204_NO_CONTENT)

        
    
#Get order in pending 

class OrderPending(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        try:
            ids=Order.objects.filter(status="pending").values_list('id', flat=True)
            orders_qs =OrderItem.objects.filter(id__in=ids).values('order','product','quantity')


            
        except OrderItem.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return print(list(orders_qs))

# Get order in process
class OrderInProcess(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        try:
            orders = Order.objects.filter(status="in process")
            
        except Order.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return orders


#Get Orders completed 
class OrderCompleted(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        try:
            orders = Order.objects.filter(status="completed")
            
        except Order.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return orders

#Get Orders delivered
class OrderDelivered(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        try:
            orders = Order.objects.filter(status="delivered")
            
        except Order.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return orders


class OrderCanceled(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        try:
            orders = Order.objects.filter(status="canceled")
            
        except Order.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return orders


#pendings with template
def datatable_static(request, *args, **kwargs):
    ids=Order.objects.filter(status="pending").values_list('id', flat=True)
    orders_qs =OrderItem.objects.filter(id__in=ids).values('order','product','quantity')

    
    return render(
        request=request,
        template_name="orders/datatable_static.html",
        context={
            "order_list": orders_qs
        })


#in process with template
def datatable_static1(request, *args, **kwargs):
    ids=Order.objects.filter(status="in process").values_list('id', flat=True)
    orders_qs =OrderItem.objects.filter(id__in=ids).values('order','product','quantity')

    
    return render(
        request=request,
        template_name="orders/datatable_static1.html",
        context={
            "order_list": orders_qs
        })



#completed with template
def datatable_static2(request, *args, **kwargs):
    ids=Order.objects.filter(status="completed").values_list('id', flat=True)
    orders_qs =OrderItem.objects.filter(id__in=ids).values('order','product','quantity')

    
    return render(
        request=request,
        template_name="orders/datatable_static2.html",
        context={
            "order_list": orders_qs
        })


#Delivered with template
def datatable_static3(request, *args, **kwargs):
    ids=Order.objects.filter(status="canceled").values_list('id', flat=True)
    orders_qs =OrderItem.objects.filter(id__in=ids).values('order','product','quantity')

    
    return render(
        request=request,
        template_name="orders/datatable_static3.html",
        context={
            "order_list": orders_qs
        })


#Canceled with template
def datatable_static4(request, *args, **kwargs):
    ids=Order.objects.filter(status="canceled").values_list('id', flat=True)
    orders_qs =OrderItem.objects.filter(id__in=ids).values('order','product','quantity')

    
    return render(
        request=request,
        template_name="orders/datatable_static4.html",
        context={
            "order_list": orders_qs
        })