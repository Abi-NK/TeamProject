from django.db import models

# Create your models here.

class Order(models.Model):

    # older models
    # orderNumber = models.IntegerField()
    # orderStatus = models.BooleanField(default=False)

    # new models
    customer_name = models.CharField(max_length=100, default="notavaliable")
    order_complete = models.BooleanField(default=False)
    time_taken = models.DateTimeField()  # The time at which the order was taken
    order_contents = models.CharField(max_length=1000, default="notavaliable")  # Includes prices as plaintext
    cooking_instructions = models.CharField(max_length=500, default="notavaliable")  # i.e Steak done medium rare or without the onions
    purchase_method = models.CharField(max_length=100, default="notavaliable")
    total_price = models.PositiveIntegerField(default=0)

    #def __str__(self):
    #    if self.orderStatus:
    #        return str(self.orderNumber) + ' - ' + 'READY'
    #    else:
    #        return str(self.orderNumber) + ' - ' + 'Not ready'

