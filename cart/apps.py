from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'

    def ready(self):
        """
        Start updater
        From Did Coding
        https://www.youtube.com/watch?v=Lzy4G1wZ7NQ&ab_channel=DidCoding
        """
        from . import updater
        updater.start()
