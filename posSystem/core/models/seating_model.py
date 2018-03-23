try:
    from django.db import models
except ImportError:
    print("failed import")

class AvailableSeatingManager(models.Manager):
    """Filter for all available seating."""
    def get_queryset(self):
        return super().get_queryset().filter(available=True)


class OccupiedSeatingManager(models.Manager):
    """Filter for all occupied seating."""
    def get_queryset(self):
        return super().get_queryset().filter(available=False)


class Seating(models.Model):
    label = models.CharField(max_length=25, default='Table 0')
    available = models.BooleanField(default=True)
    assistance = models.BooleanField(default=False)
    waiter = models.CharField(max_length=50, default="")

    objects = models.Manager()
    available_objects = AvailableSeatingManager()
    occupied_objects = OccupiedSeatingManager()

    def __str__(self):
        return self.label

    def set_unavailable(self):
        self.available = False
        self.save()
        print("%s has been taken" % self.label)

    def set_available(self):
        self.available = True
        self.save()

    def set_assistance_true(self):
        self.assistance = True
        self.save()
        print("%s requested help" % self.label)

    def set_assistance_false(self):
        self.assistance = False
        self.save()
        print("%s has been helped" % self.label)
