from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Adds dummy waiter and kitchen staff accounts to the database.'

    def handle(self, *args, **options):
        # print("Deleting all entries in User table...")
        # User.objects.all().delete()
        # print("Deleted.")

        # random names from http://namey.muffinlabs.com/
        random_names = [
            ["Jessica", "Perry"],
            ["David", "Woods"],
            ["Donna", "Lewis"],
            ["Kimberly", "White"],
            ["James", "Roberts"],
            ["Robert", "Jones"],
            ["Ruth", "Carter"],
            ["Richard", "Watson"],
            ["David", "Cox"],
            ["James", "Moore"],
            ["Elizabeth", "Sanchez"],
            ["William", "Jackson"],
            ["Lisa", "Bailey"],
            ["Betty", "Graham"],
            ["Margaret", "Jackson"],
        ]

        for i in range(1, 6):
            username = "waiter" + str(i)
            print("Adding user %s..." % username)
            try:
                User.objects.create_user(
                    username=username,
                    password="password",
                    first_name=random_names[i-1][0],
                    last_name=random_names[i-1][1],
                ).save()
            except IntegrityError:
                print("User %s is already in the database." % username)
        print("Dummy waiter accounts added.")

        for i in range(1, 6):
            username = "kitchen" + str(i)
            print("Adding user %s..." % username)
            try:
                User.objects.create_user(
                    username=username,
                    password="password",
                    first_name=random_names[i-1+5][0],
                    last_name=random_names[i-1+5][1],
                ).save()
            except IntegrityError:
                print("User %s is already in the database." % username)
        print("Dummy kitchen accounts added.")

        for i in range(1, 6):
            username = "manager" + str(i)
            print("Adding user %s..." % username)
            try:
                User.objects.create_user(
                    username=username,
                    password="password",
                    first_name=random_names[i-1+10][0],
                    last_name=random_names[i-1+10][1],
                ).save()
            except IntegrityError:
                print("User %s is already in the database." % username)
        print("Dummy manager accounts added.")
