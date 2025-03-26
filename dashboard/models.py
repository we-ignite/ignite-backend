from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class Events(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True,blank=True)
    rules = models.TextField(null=True,blank=True)
    event_date =  models.DateField(null=True,blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    tags = models.CharField(max_length=200,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    mode = models.CharField(max_length=200,null=True,blank=True)
    poster_url = models.URLField(max_length=500,null=True,blank=True)
    whatsapp_group_url = models.URLField(max_length=500,null=True,blank=True)
    
    def __str__(self):
        return f"Title: {self.title} ---- Content: {self.content} ---- Rules: {self.rules} ---- Event Date : {self.event_date} ---- From Date: {self.from_date} ---- To Date: {self.to_date} ---- Tags: {self.tags} ---- Price: {self.price} ---- Mode: {self.mode}"   
    
    
class Entries(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=200)
    members = models.TextField(null=True,blank=True)
    Mobile = models.IntegerField()
    email = models.EmailField()
    registration_date = models.DateTimeField(default=now)
    payment_status = models.BooleanField(default=False,null=True,blank=True)
    
    def __str__(self):
        return f"Event: {self.event.title} ----  Name: {self.team_name} ---- Email: {self.email} ---- Mobile: {self.Mobile}"
    
    
class Payment(models.Model):  # Capital "P"
    entry = models.ForeignKey(Entries, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=200)
    order_id = models.CharField(max_length=200)
    signature = models.CharField(max_length=200)
    
    def __str__(self):
        return f"Entry: {self.entry.team_name} ---- Payment ID: {self.payment_id} ---- Order ID: {self.order_id} ---- Signature: {self.signature}"
    

    
    

       