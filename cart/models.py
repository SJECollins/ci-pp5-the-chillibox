from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from products.models import Product, Variant


class HeldCart(models.Model):
    cart_key = models.CharField(max_length=80)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                              blank=True)
    hold_time_start = models.DateTimeField(auto_now=True)

    def check_time(self):
        time_passed = (timezone.now() - self.hold_time_start)
        return (time_passed.total_seconds() / 60.0) > settings.CART_HOLD_TIME_MINUTES


class HeldItems(models.Model):
    cart = models.ForeignKey(HeldCart, on_delete=models.CASCADE,
                             related_name='held_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE,
                                related_name='held_stock')
    qty = models.PositiveIntegerField(default=0)
    added_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.hold_time_start = self.added_on
        self.cart.save()
