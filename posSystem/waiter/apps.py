try:
    from django.apps import AppConfig
except ImportError:
    print("failed import")

class WaiterConfig(AppConfig):
    name = 'waiter'
