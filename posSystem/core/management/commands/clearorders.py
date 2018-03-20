from django.core.management.base import BaseCommand
from core.models import Order


class Command(BaseCommand):
    help = 'Resets the database to have no entries in the Order table.'

    def handle(self, *args, **options):
        print("Deleting all entries in Order table...")
        Order.objects.all().delete()
        print("Deleted.")
