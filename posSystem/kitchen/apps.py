try:
    from django.apps import AppConfig
except ImportError:
    print("failed import")

class KitchenConfig(AppConfig):
    name = 'kitchen'
