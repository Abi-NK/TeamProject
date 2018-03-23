try:
    from django.apps import AppConfig
except ImportError:
    print("failed import")

class CustomerConfig(AppConfig):
    name = 'customer'
