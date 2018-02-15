from django.db import models
import json
from customer.models import Menu, Seating
from django.utils import timezone


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

    def get_all_orders(self):
        """returns all the orders"""
        return self

    def get_kitchen_orders(self):
        """returns the orders for the kitchen"""
        return Order.objects.filter(delivered=False, confirmed=True).order_by('time')

    def get_not_confirmed_orders(self):
        """returns not confirmed orders"""
        return Order.objects.filter(confirmed=False)

    def make_order(request):
        """Create an order from the provided JSON."""
        received_json = json.loads(request.body.decode('utf-8'))
        order_json = received_json["order"]
        seating_id = received_json["tableNumber"]
        print("Recieved order: ", order_json)
        order_contents = [Menu.objects.get(pk=key) for key in order_json]
        total_price = sum([item.price * order_json[str(item.id)] for item in order_contents])
        Order(
            table=Seating.objects.get(pk=seating_id).label,
            confirmed=False,
            time=timezone.now(),
            items="<br />\n".join(["%s %s" % (order_json[str(item.id)], str(item)) for item in order_contents]),
            cooking_instructions='none',
            purchase_method='none',
            total_price=total_price,
            delivered=False,
        ).save(force_insert=True)
        print("Order taken")
