from django.db import models


class Menu(models.Model):

    # Table attributes
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=1000)
    course = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return "%s (%s)" % (self.name, self.course)
