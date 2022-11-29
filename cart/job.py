from products.models import Product, Variant
from .models import HeldCart, HeldItems


def restock():
    """
    Restock function
    Set to run every 15 minutes in updater.py
    When a cart's check_time method returns true, the holding time is over two
    hours and cart is considered abandoned.
    Restocks variants and deletes items held in carts
    Then deletes empty carts
    """
    carts = HeldCart.objects.all()

    if carts is not None:
        for cart in carts:
            if cart.check_time():
                for held_item in cart.held_items.all():
                    variant = Variant.objects.get(id=held_item.variant.id)
                    variant.current_stock += held_item.qty
                    held_item.delete()
                if not cart.held_items.exists():
                    cart.delete()
