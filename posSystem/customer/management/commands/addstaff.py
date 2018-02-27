from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Adds dummy waiter and kitchen staff accounts to the database.'

    def handle(self, *args, **options):
        for i in range(1, 6):
            username = "waiter" + str(i)
            print("Adding user %s..." % username)
            try:
                User.objects.create_user(
                    username=username,
                    password="password",
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
                ).save()
            except IntegrityError:
                print("User %s is already in the database." % username)
        print("Dummy manager accounts added.")
