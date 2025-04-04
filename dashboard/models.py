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
    customer_id = models.BigIntegerField(null=True, blank=True)  # Changed to BigIntegerField
    team_name = models.CharField(max_length=200,null=True,blank=True)
    members = models.TextField(null=True, blank=True)
    Mobile = models.BigIntegerField()  # Changed to BigIntegerField
    email = models.EmailField()
    registration_date = models.DateTimeField(default=now)
    payment_status = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return f"Event: {self.event.title} ---- Name: {self.team_name} ---- Email: {self.email} ---- Mobile: {self.Mobile} ---- Payment Status : {self.payment_status}"

    
    
class Payment(models.Model):
    entry = models.ForeignKey(Entries, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=200)  # Cashfree Payment ID
    order_id = models.CharField(max_length=200)  # Cashfree Order ID
    reference_id = models.CharField(max_length=200, blank=True, null=True)  # Cashfree Reference ID
    payment_status = models.CharField(max_length=50)  # PAID, FAILED, etc.
    payment_mode = models.CharField(max_length=100, blank=True, null=True)  # UPI, Card, NetBanking, etc.
    order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Transaction Amount
    payment_date = models.DateTimeField(auto_now_add=True)  # Timestamp when payment was recorded

    def __str__(self):
        return f"Entry: {self.entry.team_name} | Payment ID: {self.payment_id} | Status: {self.payment_status}"

    
    

       