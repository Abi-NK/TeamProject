from django.db import models
from django import forms


class Menu(models.Model):

    # Table attributes
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' - ' + self.category
