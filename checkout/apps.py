from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        """
        From CI's Boutique ado
        https://github.com/Code-Institute-Solutions/boutique_ado_v1
        """
        import checkout.signals
