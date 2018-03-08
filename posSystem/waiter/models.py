from django.db import models
from customer.models import Menu, Seating
from django.utils import timezone
from datetime import datetime, timedelta, date


class OrderItem(models.Model):
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return "%s %s" % (self.quantity, self.menu_item)

    def get_price(self):
        """Return the total price of this item."""
        return self.menu_item.price * self.quantity


class ActiveOrderManager(models.Manager):
    """Filter for all non-delivered orders."""
    def get_queryset(self):
        return super().get_queryset().filter(delivered=False)


class UnconfirmedOrderManager(models.Manager):
    """Filter for unconfirmed orders."""
    def get_queryset(self):
        return super().get_queryset().filter(confirmed=False)


class ConfirmedOrderManager(models.Manager):
    """Filter for confirmed, non-ready orders."""
    def get_queryset(self):
        return super().get_queryset().filter(confirmed=True).filter(ready_delivery=False)


class ReadyOrderManager(models.Manager):
    """Filer for ready, non-delivered orders."""
    def get_queryset(self):
        return super().get_queryset().filter(ready_delivery=True).filter(delivered=False)


class DeliveredTodayOrderManager(models.Manager):
    """Filter for today's delivered orders."""
    def get_queryset(self):
        return super().get_queryset().filter(delivered=True).filter(time__date=date.today())


class DeliveredWeekOrderManager(models.Manager):
    """Filter for this week's delivered orders."""
    def get_queryset(self):
        return super().get_queryset().filter(delivered=True).filter(
            time__date__gt=timezone.now().date()-timedelta(days=7)
        )


class CancelledTodayOrderManager(models.Manager):
    """Filter for today's cancelled orders."""
    def get_queryset(self):
        return super().get_queryset().filter(cancelled=True).filter(time__date=date.today())


class CancelledWeekOrderManager(models.Manager):
    """Filter for this week's cancelled orders."""
    def get_queryset(self):
        return super().get_queryset().filter(cancelled=True).filter(
            time__date__gt=timezone.now().date()-timedelta(days=7)
        )


class Order(models.Model):

    objects = models.Manager()
    active_objects = ActiveOrderManager()
    confirmed_objects = ConfirmedOrderManager()
    unconfirmed_objects = UnconfirmedOrderManager()
    ready_objects = ReadyOrderManager()
    delivered_today_objects = DeliveredTodayOrderManager()
    delivered_week_objects = DeliveredWeekOrderManager()
    cancelled_today_objects = CancelledTodayOrderManager()
    cancelled_week_objects = CancelledWeekOrderManager()

    table = models.ForeignKey(Seating, on_delete=models.CASCADE)
    time = models.DateTimeField()  # The time at which the order was taken
    items = models.ManyToManyField(OrderItem)
    cooking_instructions = models.CharField(max_length=500, default='na')  # Preferences, allergies, etc.
    purchase_method = models.CharField(max_length=100, default='na')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    confirmed = models.BooleanField(default=False)  # order has been confirmed
    cancelled = models.BooleanField(default=False)
    ready_delivery = models.BooleanField(default=False)  # order is ready for delivery
    delivered = models.BooleanField(default=False)  # order has been delivered

    def __str__(self):
        status = ""
        if self.cancelled:
            status = "cancelled"
        elif self.delivered:
            status = "delivered"
        elif self.ready_delivery:
            status = "ready for delivery"
        elif self.confirmed:
            status = "preparing"
        else:
            status = "unconfirmed"
        return "Order #%s: %s, status: %s, price: %s, time placed: %s" % \
            (self.id, self.table, status, self.get_price_display(), self.time)

    def set_confirmed(self):
        """sets the order as confirmed"""
        self.confirmed = True
        self.save()
        print("Order %s is confirmed" % self.id)

    # Set cancelled in db
    def set_cancelled(self):
        """sets the order as cancelled"""
        self.cancelled = True
        self.save()
        print("Order %s is cancelled" % self.id)

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

    def make_order(order_json, seating_id):
        """Create an order from the provided JSON."""
        order_contents = [Menu.objects.get(pk=key) for key in order_json]
        total_price = sum([item.price * order_json[str(item.id)] for item in order_contents])
        order = Order.objects.create(
            # table=Seating.objects.get(pk=seating_id).label,
            table = Seating.objects.get(pk=seating_id),
            confirmed=False,
            time=timezone.now(),
            cooking_instructions='none',
            purchase_method='none',
            total_price=total_price,
            delivered=False,
        )
        for menu_id, quantity in order_json.items():
            order_item = OrderItem.objects.create(
                menu_item=Menu.objects.get(pk=menu_id),
                quantity=quantity
            )
            order.items.add(order_item)
        order.save()

    def get_time_display(self):
        """Get the time the order was placed in a displayable format."""
        return str(self.time)[11: 19]

    def get_price_display(self):
        """Get the price in a displayable format."""
        return "£%.2f" % self.total_price

    def get_items_display(self):
        """Return the string representation of the items in the order."""
        return "\n".join([str(item) for item in self.items.all()])

    def is_nearly_late(self):
        allowed_gap = timedelta(minutes=7)
        difference = datetime.now() - self.time.replace(tzinfo=None)
        return difference >= allowed_gap

    def is_late(self):
        allowed_gap = timedelta(minutes=10)
        difference = datetime.now() - self.time.replace(tzinfo=None)
        return difference >= allowed_gap


class Payment(models.Model):

    order = models.OneToOneField(Order, on_delete=models.CASCADE)   # order of payment
    card_holder = models.CharField(max_length=50, default='na')     # name of card holder
    card_number = models.CharField(max_length=12, default='na')     # Card number
    cvc = models.CharField(max_length=3, default='na')              # CVC
    expiry = models.CharField(max_length=5, default='na')           # Card expiry date
    terms_conditions = models.BooleanField(default=False)           # Customer has accepted t and c
    payment_requested = models.BooleanField(default=False)          # Waiter has asked for payment
    payment_received = models.BooleanField(default=False)           # Payment information has been received
    payment_accepted = models.BooleanField(default=False)           # Waiter has accepted the payment

    def __str__(self):
       return "Order: %s, Accepted: %s" % (self.order.id, self.payment_accepted)

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
