from django.core.management.base import BaseCommand
from customer.models import Seating


class Command(BaseCommand):
    help = 'Marks all seating in the Seating table as available'

    def handle(self, *args, **options):
        print("Marking all seating as available...")
        seating = Seating.objects.filter(available=False)
        for seat in seating:
            seat.available = True
            seat.save()
        print("Done.")
