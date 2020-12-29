from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=400, null=True)
    phone = models.CharField(max_length=400, null=True)
    email = models.CharField(max_length=400, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

