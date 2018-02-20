from django.db import models


class Menu(models.Model):

    # Table attributes
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=1000)
    course = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    allergy = models.CharField(max_length=1000, default="")
    calories = models.IntegerField(default=0)
    image = models.CharField(max_length=1000)

    def __str__(self):
        return "%s (%s)" % (self.name, self.course)


class AvailableSeatingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True)


class Seating(models.Model):
    label = models.CharField(max_length=25, default='Table 0')
    available = models.BooleanField(default=True)
    assistance = models.BooleanField(default=False)

    objects = models.Manager()
    available_objects = AvailableSeatingManager()

    def __str__(self):
        return self.label

    def set_unavailable(self):
        self.available = False
        self.save()
        print("%s has been taken" % self.label)

    def set_assistance_true(self):
        self.assistance = True
        self.save()
        print("%s requested help" % self.label)
