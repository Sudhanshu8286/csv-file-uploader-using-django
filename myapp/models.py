# from django.db import models

from django.contrib.auth.models import User
from django.db import models


class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()


class CustomerDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    



    
    def __str__(self):
        return self.email