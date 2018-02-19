from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Adds dummy waiter and kitchen staff accounts to the database.'

    def handle(self, *args, **options):
        for i in range(1, 6):
            username = "waiter" + str(i)
            print("Adding user %s..." % username)
            User.objects.create_user(
                username=username,
                password="password",
            ).save()
        print("Dummy waiter accounts added.")

        for i in range(1, 6):
            username = "kitchen" + str(i)
            print("Adding user %s..." % username)
            User.objects.create_user(
                username=username,
                password="password",
            ).save()
        print("Dummy kitchen accounts added.")
