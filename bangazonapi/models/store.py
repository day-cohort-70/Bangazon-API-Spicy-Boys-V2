from django.db import models
from django.conf import settings
from .customer import Customer
from django.contrib.auth.models import User

# Import the User model if you haven't customized it


class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2500)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, related_name="store_owned"
    )

   # def __str__(self):
    #    return self.description

