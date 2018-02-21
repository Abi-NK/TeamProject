from django.db import models
from datetime import datetime, timedelta


class Order(models.Model):

    # Order db
    table = models.CharField(max_length=100, default='na')
    time = models.DateTimeField()  # The time at which the order was taken
    items = models.CharField(max_length=1000, default='na')  # Includes prices as plaintext
    cooking_instructions = models.CharField(max_length=500, default='na')  # i.e Steak done medium
    #  rare or without the onions
    purchase_method = models.CharField(max_length=100, default='na')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    confirmed = models.BooleanField(default=False)  # order has been confirmed
    ready_delivery = models.BooleanField(default=False)  # order is ready for delivery
    delivered = models.BooleanField(default=False)  # order has been delivered

    def __str__(self):
        if self.confirmed:
            return "Order: " + str(self.id) + ' -> ' + 'READY'
        else:
            return "Order: " + str(self.id) + ' -> ' + 'Not ready'

    def set_confirmed(self):
        """sets the order as confirmed"""
        self.confirmed = True
        self.save()
        print("Order %s is confirmed" % self.id)

    def set_ready_delivery(self):
        """sets the order as ready to be delivered"""
        self.ready_delivery = True
        self.save()
        print("Order %s is ready for delivery" % self.id)

    def set_delivered(self):
        """sets the order as delivered"""
        self.delivered = True
        self.save()
        print("Order %s is has been delivery" % self.id)

    def get_time_display(self):
        """Get the time the order was placed in a displayable format."""
        return str(self.time)[11: 19]

    def get_price_display(self):
        """Get the price in a displayable format."""
        return "£%.2f" % self.total_price

    def is_nearly_late(self):
        allowed_gap = timedelta(minutes=7)
        difference = datetime.now() - self.time.replace(tzinfo=None)
        return difference >= allowed_gap

    def is_late(self):
        allowed_gap = timedelta(minutes=10)
        difference = datetime.now() - self.time.replace(tzinfo=None)
        return difference >= allowed_gap
