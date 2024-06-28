from django.db import models
from django.conf import settings




class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2500)
    customer = models.OneToOneField(
        "customer", on_delete=models.CASCADE, related_name="store_owned"
    )
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description
