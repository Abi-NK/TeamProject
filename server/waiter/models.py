from django.db import models

# Create your models here.

class Order(models.Model):

    # older models
    # orderNumber = models.IntegerField()
    # orderStatus = models.BooleanField(default=False)

    # new models
    customer_name = models.CharField(max_length=100, default='na')
    order_complete = models.BooleanField(default=False)
    time_taken = models.DateTimeField()  # The time at which the order was taken
    order_contents = models.CharField(max_length=1000, default='na')  # Includes prices as plaintext
    cooking_instructions = models.CharField(max_length=500, default='na')  # i.e Steak done medium
    #  rare or without the onions
    purchase_method = models.CharField(max_length=100, default='na')
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self): # HOW do i accsess the order number?
        if self.order_complete:
            return "Order: " + str(self.id) + ' -> ' + 'READY'
        else:
            return "Order: " + str(self.id) + ' -> ' + 'Not ready'

