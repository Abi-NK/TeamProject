
from django.core.management.base import BaseCommand
from customer.models import Menu
from waiter.models import Order

sample_menu = [
    {"name": "Pork Pibil", "price": 7.80, "course": "main", "category": "Burritos"},
]


class Command(BaseCommand):
    args = ''
    help = 'resets the database to have no orders and rebuilds the menu'

    def _create_tags(self):
        Order.objects.all().delete()
        print("Order table cleared.")

        Menu.objects.all().delete()
        print("Menu table cleared, repopulating...")
        for item in sample_menu:
            Menu(
                name=item["name"],
                price=item["price"],
                type=item["course"],
                category=item["category"]
            ).save()
        print(Menu.objects.all())

        print("Database reset complete.")

    def handle(self, *args, **options):
        self._create_tags()
