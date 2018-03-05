from django.db import models
import json
from customer.models import Menu, Seating
from django.utils import timezone


class Order(models.Model):

    # Order db
    items = models. ManyToManyField(Menu)
    # table = models.OneToOneField(Seating, on_delete=models.CASCADE)
    #table = models.CharField(max_length=100, default='na')
    time = models.DateTimeField()  # The time at which the order was taken
    #items = models.CharField(max_length=1000, default='na')  # Includes prices as plaintext
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
        # return self
        return Order.objects.all()

    def get_ready_orders(self):
        """returns all the ready orders"""
        return Order.objects.filter(confirmed=True)

    def get_kitchen_orders(self):
        """returns the orders for the kitchen"""
        return Order.objects.filter(delivered=False, confirmed=True).order_by('time')

    def get_not_confirmed_orders(self):
        """returns not confirmed orders"""
        return Order.objects.filter(confirmed=False)

    def make_order(request):
        """Create an order from the provided JSON."""
        if "seating_id" not in request.session:
            print("A session without a seating ID tried to place an order.")
            return HttpResponseNotFound("no seating_id in session")

        order_json = json.loads(request.body.decode('utf-8'))["order"]
        print("Recieved order: ", order_json)
        order_contents = [Menu.objects.get(pk=key) for key in order_json]
        total_price = sum([item.price * order_json[str(item.id)] for item in order_contents])
        Order(
            # table=Seating.objects.get(pk=request.session["seating_id"]).label,
            table=Seating.objects.get(pk=request.session["seating_id"]),
            confirmed=False,
            time=timezone.now(),
            items="<br />\n".join(["%s %s" % (order_json[str(item.id)], str(item)) for item in order_contents]),
            cooking_instructions='none',
            purchase_method='none',
            total_price=total_price,
            delivered=False,
        ).create(force_insert=True)


class Payment(models.Model):

    # payment db
    # table = models.OneToOneField(Seating, on_delete=models.CASCADE)
    table = models.CharField(max_length=50, default='na') #- commented for attempting db keys
    order = models.CharField(max_length=50, default='na') #- commented for attempting db keys
    card_holder = models.CharField(max_length=50, default='na')     # name of card holder
    card_number = models.CharField(max_length=12, default='na')     # Card number
    cvc = models.CharField(max_length=3, default='na')              # CVC
    expiry = models.CharField(max_length=5, default='na')           # Card expiry date
    terms_conditions = models.BooleanField(default=False)           # Customer has accepted t and c
    payment_requested = models.BooleanField(default=False)          # Waiter has asked for payment
    payment_received = models.BooleanField(default=False)           # Payment information has been received
    payment_accepted = models.BooleanField(default=False)           # Waiter has accepted the payment

    def get_payments(self):
        """Returns all the payments"""
        print("Payments sent")
        return Payment.objects.all()

    def get_card_holder(self):
        return self.card_holder()

    def get_card_number(self):
        return self.card_number()

    def get_cvc(self):
        return self.cvc()

    def get_card_expiry(self):
        return self.expiry()

    def get_t_and_c(self):
        return self.terms_conditions()

    def get_payment_requested(self):
        return self.payment_received()

    def get_payment_received(self):
        return self.payment_received()

    def get_payment_accepted(self):
        return self.payment_accepted()

    def set_t_and_c(self):
        """Sets the terms and conditions to be accepted"""
        self.terms_conditions = True
        self.save()
        print("Customer %s has accepted the Terms and conditions" % self.id)

    def set_payment_requested(self):
        """Sets the payment to be requested"""
        self.payment_requested = True
        self.save()
        print("Customer %s payment has been requested" % self.id)

    def set_payment_received(self):
        """Sets the payment to be received"""
        self.payment_received = True
        self.save()
        print("Customer %s payment has been received" % self.id)

    def set_payment_accepted(self):
        """Sets the payment to be accepted"""
        self.payment_accepted = True
        self.save()
        print("Customer %s payment has been accepted" % self.id)
