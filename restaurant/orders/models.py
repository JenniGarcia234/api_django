from django.db import models
from products.models import Product

# Create your models here.
ORDER_STATUS_CHOICES = (
('pending', 'Pending'),
('in process', 'In Process'),
('completed', 'Completed'),
('delivered', 'Delivered'),
('canceled', 'Canceled'),
)

class Order(models.Model):
    date_ordered = models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='pending')
    total=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    activate=models.BooleanField(null=True, default=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=models.Manager()


class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    activate=models.BooleanField(null=True, default=True)
    quantity=models.IntegerField(default=0, null=True, blank=True) 
    objects= models.Manager()
