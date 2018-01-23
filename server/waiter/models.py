from django.db import models

# Create your models here.

class order(models.Model):

    orderNumber = models.IntegerField()
    orderStatus = models.BooleanField(default=False)
