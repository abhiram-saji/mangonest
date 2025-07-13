from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserType(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    type = models.CharField(max_length=50,null=True)

class user_reg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=50,null=True)
    phone = models.CharField(max_length=50,null=True)

class shop_reg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=50,null=True)
    phone = models.CharField(max_length=50,null=True)
    image=models.ImageField(max_length=50,null=True)
    shop_owner_name = models.CharField(max_length=50,null=True)
    city=models.CharField(max_length=50,null=True)
    

class Fruits(models.Model):
    user = models.ForeignKey(shop_reg, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField(null=True)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    discount = models.IntegerField(null=True)
    description = models.TextField(max_length=500)
    image = models.ImageField(blank=True, null=True)
    discountprice = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    product = models.ForeignKey(Fruits, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(user_reg, on_delete=models.CASCADE,null=True)
    quantity = models.CharField(max_length=50,null=True) 
    totalprice=models.CharField(max_length=50,null=True) 
    action=models.CharField(max_length=50,null=True)
    status=models.CharField(max_length=50,null=True,default='Processing')

    created_at = models.DateTimeField(auto_now_add=True)

    
class Feedback(models.Model):
    user = models.ForeignKey(user_reg, on_delete=models.CASCADE,null=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,null=True)
    reaction = models.CharField(max_length=20)
    feedback_message = models.TextField()
