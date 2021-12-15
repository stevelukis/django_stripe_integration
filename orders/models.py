from django.db import models

from product.models import Product


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    checkout_session = models.CharField(max_length=200, unique=True)
    paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
