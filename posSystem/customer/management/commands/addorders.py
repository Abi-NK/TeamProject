from django.core.management.base import BaseCommand
from customer.models import Menu, Seating
from waiter.models import Order
import random
from django.utils import timezone
from datetime import timedelta


def random_order_json():
    menu_items = [item for item in Menu.objects.all()]
    random.shuffle(menu_items)
    order = {}
    for i in range(random.randrange(1, 11)):
        order[str(menu_items[i].id)] = random.choice([1, 1, 1, 1, 1, 1, 1, 2, 2, 3])
    return order


def items_string_from_json(order_json):
    order_contents = [Menu.objects.get(pk=key) for key in order_json]
    return "\n".join(["%s %s" % (order_json[str(item.id)], str(item)) for item in order_contents])


def total_price_from_json(order_json):
    order_contents = [Menu.objects.get(pk=key) for key in order_json]
    return sum([item.price * order_json[str(item.id)] for item in order_contents])


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
        random.shuffle(all_seating)
        table_count = len(all_seating)

        # mark some tables as taken and generate an order for each table
        dummy_table_count = random.randrange(int(table_count * 0.5), int(table_count * 0.75 + 1))
        for i in range(dummy_table_count):
            seating = all_seating[i]
            seating.set_unavailable()
            order_json = random_order_json()
            time_offset = (dummy_table_count - i) / dummy_table_count * 30
            order = Order.objects.create(
                table=seating.label,
                time=timezone.now() - timedelta(minutes=time_offset),
                items=items_string_from_json(order_json),
                total_price=total_price_from_json(order_json),
                confirmed=False,
                ready_delivery=False,
                delivered=False,
            )
            print(str(order))

            # occasionally add an extra order for the current table
            if random.random() < 0.25:
                order_json = random_order_json()
                time_offset = (dummy_table_count - i) / dummy_table_count * 30
                order = Order.objects.create(
                    table=seating.label,
                    time=timezone.now() - timedelta(minutes=time_offset),
                    items=items_string_from_json(order_json),
                    total_price=total_price_from_json(order_json),
                    confirmed=False,
                    ready_delivery=False,
                    delivered=False,
                )
                print(str(order))

        all_orders = [item for item in Order.objects.all()]
        random.shuffle(all_orders)
        order_count = len(all_orders)

        # mark some active orders to be confirmed / ready / delivered
        for i in range(order_count):
            order = all_orders[i]
            if i < order_count * 0.7:
                order.confirmed = True
            if i < order_count * 0.3:
                order.ready_delivery = True
            if i < order_count * 0.1:
                order.delivered = True
            order.save()
            print(str(order))
