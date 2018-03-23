try:
    from django.apps import AppConfig
except ImportError:
    print("failed import")

class CoreConfig(AppConfig):
    name = 'core'
