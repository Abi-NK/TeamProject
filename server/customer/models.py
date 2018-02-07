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

    def __str__(self):
        return "%s (%s)" % (self.name, self.course)


class Seating(models.Model):
    label = models.CharField(max_length=25, default='Table 0')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.label
