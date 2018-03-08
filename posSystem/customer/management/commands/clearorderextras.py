from django.core.management.base import BaseCommand
from waiter.models import OrderExtra


class Command(BaseCommand):
    help = 'Resets the database to have no entries in the OrderExtra table.'

    def handle(self, *args, **options):
        print("Deleting all entries in OrderExtra table...")
        OrderExtra.objects.all().delete()
        print("Deleted.")
