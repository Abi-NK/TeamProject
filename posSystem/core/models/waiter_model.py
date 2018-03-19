from django.db import models
from core.models import Seating, User


class Waiter(models.Model):
    onduty = models.BooleanField(default=False)
    name = models.CharField(max_length=50, default='waiter1')

    def __str__(self):
        return "%s: %s" % (self.name, "on duty" if self.onduty else "off duty")

    def set_waiter_on_duty(self):
        """Set the waiter to be on duty."""
        self.onduty = True
        self.save()
        print("waiter %s is on duty" % self.name)

    def set_waiter_off_duty(self):
        """Set the waiter to be off duty."""
        for seating in Seating.objects.all():
            if seating.waiter == self.name:
                seating.waiter = ""
                seating.save()
        self.onduty = False
        self.save()
        print("waiter %s is off duty" % self.name)

    def get_full_name(self):
        return User.objects.get(username=self.name).get_full_name()
