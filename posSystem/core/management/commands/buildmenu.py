from django.core.management.base import BaseCommand
from core.models import Menu
import json
import random


class Command(BaseCommand):
    help = 'Clears and repopulates the Menu table with a sample menu.'

    with open("samplemenu.json") as menu_file:
        sample_menu = json.load(menu_file)

    def handle(self, *args, **options):
        print("Deleting all entries in Menu table...")
        Menu.objects.all().delete()
        print("Deleted.")
        for item in self.sample_menu:
            print("Adding %s (%s)..." % (item[0], item[3]))
            Menu(
                name=item[0],
                price=item[1],
                description=item[2],
                course=item[3],
                category=item[4],
                allergy=item[5],
                calories=item[6],
                image=item[7],
                vegetarian=item[8],
                vegan=item[9],
                meat=item[10],
                stock=random.randrange(20, 31),
            ).save()
        print("Sample menu added.")
