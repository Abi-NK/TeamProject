from django.core.management.base import BaseCommand
from customer.models import Seating


class Command(BaseCommand):
    help = 'Clears and repopulates the Seating table with sample seating.'

    def handle(self, *args, **options):
        print("Deleting all entries in Seating table...")
        Seating.objects.all().delete()
        print("Deleted.")

        for i in range(1, 21):
            print("Adding Table " + str(i))
            Seating(
                label=("Table " + str(i))
            ).save()
        print("Sample seating added.")
