try:
    from django.apps import AppConfig
except ImportError:
    print("failed import")

class ManagerConfig(AppConfig):
    name = 'manager'
