from django.db import models
from django.conf import settings

# Import the User model if you haven't customized it


class Store(models.Model):
    description = models.CharField(max_length=255)
    customer_id = models.ForeignKey(
        "customer", on_delete=models.CASCADE, related_name="stores"
    )

    def __str__(self):
        return self.description