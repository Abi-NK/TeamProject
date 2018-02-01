from django.core.management.base import BaseCommand
from customer.models import Menu


class Command(BaseCommand):
    help = 'Clears and repopulates the Menu table with a sample menu.'

    def handle(self, *args, **options):
        print("Deleting all entries in Menu table...")
        Menu.objects.all().delete()
        print("Deleted.")
        print("Adding sample menu item...")
        Menu(
            name="Pork pibil",
            price=7.80,
            description="Slow cooked, with pink pickled onions",
            course="Main",
            category="Burritos"
        ).save()
        print("Added.")
