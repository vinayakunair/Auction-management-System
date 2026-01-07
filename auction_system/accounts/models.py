from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20,unique=True)
    email = models.CharField(unique=True)

    ROLE_CHOICES = (
        ('admin','Admin'),
        ('buyer','Buyer'),
        ('seller','Seller'),
    )

    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='buyer')