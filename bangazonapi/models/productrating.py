from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .customer import Customer


class ProductRating(models.Model):

    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="ratings")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    review = models.TextField()

class Meta:
    verbose_name = ("productrating")
    verbose_name_plural = ("productratings")
    unique_together = ('customer', 'product')

def __str__(self):
    return self.rating
