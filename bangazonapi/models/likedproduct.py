from django.db import models


class LikedProduct(models.Model):
    customer_id = models.ForeignKey("Customer", on_delete=models.CASCADE)
    product_id = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "LikedProduct"
