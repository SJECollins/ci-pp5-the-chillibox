from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    From CI's boutique ado
    https://github.com/Code-Institute-Solutions/boutique_ado_v1
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    From CI's boutique ado
    https://github.com/Code-Institute-Solutions/boutique_ado_v1
    """
    instance.order.update_total()
