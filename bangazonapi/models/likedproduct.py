from django.db import models


class LikedProduct(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "likedproduct"
