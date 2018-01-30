from django.db import models


class Order(models.Model):

    # Order db
    table = models.CharField(max_length=100, default='na')
    complete = models.BooleanField(default=False)  # weather or not the order is ready to be delivered
    time = models.DateTimeField()  # The time at which the order was taken
    items = models.CharField(max_length=1000, default='na')  # Includes prices as plaintext
    cooking_instructions = models.CharField(max_length=500, default='na')  # i.e Steak done medium
    #  rare or without the onions
    purchase_method = models.CharField(max_length=100, default='na')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivered = models.BooleanField(default=False)  # weather or not the order has been delivered
    table_assistance = models.BooleanField(default=False)  # if the table needs help

    def __str__(self):
        if self.complete:
            return "Order: " + str(self.id) + ' -> ' + 'READY'
        else:
            return "Order: " + str(self.id) + ' -> ' + 'Not ready'

