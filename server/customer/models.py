from django.db import models
from django import forms


class Menu(models.Model):

    # Table attributes
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    course = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' - ' + self.category
