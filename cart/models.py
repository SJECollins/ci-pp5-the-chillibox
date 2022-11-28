from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from products.models import Product, Variant


class HeldCart(models.Model):
    cart_key = models.CharField(max_length=32)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                              blank=True)
    hold_time_start = models.DateTimeField(auto_now_add=True)

    def check_time(self):
        return (timezone.now() - self.hold_time_start) > settings.CART_HOLD_TIME_MINUTES


class HeldItems(models.Model):
    cart = models.ForeignKey(HeldCart, on_delete=models.CASCADE,
                             related_name='held_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE,
                                related_name='held_stock')
    qty = models.PositiveIntegerField(default=0)
