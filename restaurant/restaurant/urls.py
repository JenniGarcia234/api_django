"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from products.views import ProductsList, CategoryListApiView,  ProductDetail
from orders.views import OrderList, OrderItemL, OrderPending, OrderItemDetail,OrderDetail, datatable_static, datatable_static1, datatable_static2, datatable_static3, datatable_static4
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/product-list/', ProductsList.as_view(), name='product_list'),
    path('api/product-detail/<int:id>', ProductDetail.as_view(), name='product_detail'),
    path('api/category-list/', CategoryListApiView.as_view(), name='category_list'),
    path('api/orders/', OrderList.as_view(), name='order_list'),
    path('api/orders-detail/<int:id>', OrderDetail.as_view(), name='order_detail'),
    path('api/orderitem/<int:order_id>', OrderItemL.as_view(), name='order_item'),
    path('api/ordersitem/<int:id>/', OrderItemDetail.as_view(), name='orderitem_detail'),
    path('api/order-pending/', OrderPending.as_view(), name='order-pending'),
    

    #Prueba
    path('static', datatable_static, name='datatable_static'),
    path('static1', datatable_static1, name='datatable_static1'),
    path('static2', datatable_static2, name='datatable_static2'),
    path('static3', datatable_static1, name='datatable_static3'),
    path('static4', datatable_static1, name='datatable_static4'),

]
