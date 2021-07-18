from django.db import models


# Create your models here.
class Category(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(unique=True, max_length=150)
    objects=models.Manager()
    def __str__(self):
        return self.title

class Product(models.Model):
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=13,help_text="Enter Stock Keeping Unit")    
    name = models.CharField(max_length=200, help_text="Enter product name")
    description = models.TextField(help_text="Enter product description")
    buyPrice = models.DecimalField(decimal_places=2, max_digits=20,help_text="Enter product price per unit")
    quantity = models.IntegerField(help_text="Enter quantity")
    objects=models.Manager()

    def __str__(self):
        return self.name