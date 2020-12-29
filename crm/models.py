from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=400)
    phone = models.CharField(max_length=400)
    email = models.CharField(max_length=400)

