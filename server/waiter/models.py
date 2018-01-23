from django.db import models

# Create your models here.

class Order(models.Model):

    orderNumber = models.IntegerField()
    orderStatus = models.BooleanField(default=False)

    def __str__(self):
        if self.orderStatus:
            return str(self.orderNumber) + ' - ' + 'READY'
        else:
            return str(self.orderNumber) + ' - ' + 'Not ready'
