from django.core.management.base import BaseCommand
from customer.models import Seating
from waiter.models import Order
import random
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populates the Order table with sample orders.'

    def handle(self, *args, **options):
        # clear out the existing orders
        print("Deleting all entries in Order table...")
        Order.objects.all().delete()
        print("Deleted.")

        # free up all tables to ensure there are some left at the end
        print("Marking all seating as available...")
        for seat in Seating.objects.all():
            seat.set_available()
        print("Done.")

        all_seating = [item for item in Seating.objects.all()]
        number_of_tables = len(all_seating)
        random.shuffle(all_seating)
        print("Available tables: %s" % number_of_tables)

        for i in range(random.randrange(number_of_tables * 0.5, number_of_tables * 0.75 + 1)):
            seating = all_seating[i]
            seating.set_unavailable()
            order = Order.objects.create(table=seating.label, time=timezone.now(), total_price=10.00)
            print(str(order))

        print("Available tables: %s" % len(Seating.available_objects.all()))
