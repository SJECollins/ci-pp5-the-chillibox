import uuid
from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product, Variant
from profiles.models import UserProfile


class Order(models.Model):
    """
    Order model from CI boutique_ado
    """
    order_number = models.CharField(max_length=32, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    country = CountryField(blank_label='Country *')
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40)
    street_address1 = models.CharField(max_length=80)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6,
                                        decimal_places=2, default=0)
    order_total = models.DecimalField(max_digits=10,
                                      decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10,
                                      decimal_places=2, default=0)

    def _generate_order_number(self):
        """
        Generate an order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        !! Revisit this if considering allowing sales !!
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = Decimal(settings.STANDARD_DELIVERY_COST)
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number if not set
        already
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    OrderLineItem model from CI boutique_ado
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         editable=False)

    def save(self, *args, **kwargs):
        """
        Override save method to set lineitem total and update order total
        """
        self.lineitem_total = self.variant.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} in order {self.order.order_number}'
