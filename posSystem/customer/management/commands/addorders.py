from django.core.management.base import BaseCommand
from customer.models import Menu, Seating
from waiter.models import Order, OrderItem
import random
from django.utils import timezone
from datetime import date, datetime, time, timedelta


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
                total_price=total_price_from_json(order_json),
                confirmed=False,
                ready_delivery=False,
                delivered=False,
            )
            for menu_id, quantity in order_json.items():
                order_item = OrderItem.objects.create(
                    menu_item=Menu.objects.get(pk=menu_id),
                    quantity=quantity
                )
                order.items.add(order_item)
            order.save()
            print(str(order))

            # occasionally add an extra order for the current table
            if random.random() < 0.25:
                order_json = random_order_json()
                time_offset = (dummy_table_count - i) / dummy_table_count * 30
                order = Order.objects.create(
                    table=seating.label,
                    time=timezone.now() - timedelta(minutes=time_offset),
                    total_price=total_price_from_json(order_json),
                    confirmed=False,
                    ready_delivery=False,
                    delivered=False,
                )
                for menu_id, quantity in order_json.items():
                    order_item = OrderItem.objects.create(
                        menu_item=Menu.objects.get(pk=menu_id),
                        quantity=quantity
                    )
                    order.items.add(order_item)
                order.save()
                print(str(order))

        all_orders = [item for item in Order.objects.all()]
        random.shuffle(all_orders)
        order_count = len(all_orders)

        # mark some active orders to be confirmed / ready / delivered, and about 1/10th to be cancelled
        for i in range(order_count):
            order = all_orders[i]
            if i < order_count * 0.7:
                order.confirmed = True
            if i < order_count * 0.3:
                order.ready_delivery = True
            if i < order_count * 0.1:
                order.delivered = True
            if random.random() < 0.1:
                order.cancelled = True
            order.save()
            print(str(order))

        # create a history of delivered orders
        orders_per_day = [25, 50]
        days_of_history = 7

        all_seating = [item for item in Seating.objects.all()]
        random.shuffle(all_seating)
        table_count = len(all_seating)
        date_now = date.today()

        for i in range(days_of_history):
            day_offset = timedelta(days=i)
            order_date = date_now - day_offset
            for j in range(random.randrange(orders_per_day[0], orders_per_day[1])):
                order_json = random_order_json()
                random_hour = random.randrange(8, 23)
                random_minute = random.randrange(60)
                random_second = random.randrange(60)
                order_time = time(hour=random_hour, minute=random_minute, second=random_second)
                combined = datetime.combine(order_date, order_time)
                order_datetime = timezone.make_aware(combined, timezone.get_default_timezone())
                order = Order.objects.create(
                    table=all_seating[random.randrange(table_count)].label,
                    time=order_datetime,
                    total_price=total_price_from_json(order_json),
                    confirmed=True,
                    ready_delivery=True,
                    delivered=True,
                )
                if random.random() < 0.1:
                    order.cancelled = True
                    order.save()
                print(str(order))
