from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class events(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True,blank=True)
    rules = models.TextField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    tags = models.CharField(max_length=200,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    mode = models.CharField(max_length=200,null=True,blank=True)
    
    def __str__(self):
        return f"Title: {self.title} ---- Content: {self.content} ---- Rules: {self.rules} ---- From Date: {self.from_date} ---- To Date: {self.to_date} ---- Tags: {self.tags} ---- Price: {self.price} ---- Mode: {self.mode}"   
    
    
class entries(models.Model):
    event = models.ForeignKey(events, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    Mobile = models.IntegerField()
    
    def __str__(self):
        return f"Event: {self.event.title} ----  Name: {self.name} ---- Email: {self.email} ---- Mobile: {self.Mobile}"
    
    
    

       