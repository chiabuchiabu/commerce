from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchitem=models.ManyToManyField('auction_list',related_name="watch_list",blank=True) 


class auction_list(models.Model):
    title=models.CharField(max_length=64)
    description=models.TextField()
    startbidprice=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.CharField(max_length=64)
    url=models.URLField(max_length=600)
    up_date=models.DateTimeField(auto_now_add=True)
    seller=models.ForeignKey(User,on_delete=models.CASCADE,related_name="solder",null=True,blank=True)
    highestbid=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    highestbider=models.CharField(max_length=150,null=True,blank=True)

    
    def __str__(self):
        return f"{self.title}  _{self.seller}_{self.id}"
    
    
   
#deal with bid 
class Bid(models.Model):
    title=models.ForeignKey(auction_list,on_delete=models.CASCADE,related_name="titlee")
    buyer=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bider",null=True,blank=True)
    bid_price=models.DecimalField(max_digits=10,decimal_places=2)
    create_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.buyer} bid {self.title} in {self.bid_price}"

class Comment(models.Model):
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userc",blank=True,null=True)
    title=models.ForeignKey(auction_list,on_delete=models.CASCADE,related_name="titlec")
    create_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.user} :{self.title}"

class Active(models.Model):
    title=models.ForeignKey("auction_list",on_delete=models.CASCADE,related_name="titlea")
    active=models.BooleanField(default=True)
    time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"