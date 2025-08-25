# 代码生成时间: 2025-08-26 02:16:39
from django.apps import AppConfig


class ShoppingCartAppConfig(AppConfig):
    """Django application configuration for ShoppingCartApp."""
    name = 'shopping_cart_app'
    verbose_name = 'Shopping Cart Application'

    def ready(self):
        from . import signals  # Import signal handlers
        # Any additional setup can be done here
