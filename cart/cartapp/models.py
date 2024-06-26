from django.db import models
from django.contrib.auth.models import User
class ProductModel(models.Model):
    pname =  models.CharField(max_length=100, default='')
    pprice = models.IntegerField(default=0)
    pimages = models.CharField(max_length=100, default='')
    pdescription = models.TextField(blank=True, default='')
    def __str__(self):
        return self.pname
        
class OrdersModel(models.Model):
    subtotal = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    grandtotal = models.IntegerField(default=0)
    customname =  models.CharField(max_length=100, default='')
    customemail =  models.CharField(max_length=100, default='')
    customaddress =  models.CharField(max_length=100, default='')
    customphone =  models.CharField(max_length=100, default='')
    paytype =  models.CharField(max_length=50, default='')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_completed_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order_id: {self.id}, customname: {self.customname}"
     
class DetailModel(models.Model):
    dorder = models.ForeignKey(OrdersModel, on_delete=models.CASCADE)
    #sqlite
    # dorder = models.ForeignKey('OrdersModel', on_delete=models.CASCADE)

    pname = models.CharField(max_length=100, default='')
    unitprice = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    dtotal = models.IntegerField(default=0)
    def __str__(self):
        return self.pname
