from django.db import models
from customer.models import Menu, Seating
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, date


class Waiter(models.Model):
    onduty = models.BooleanField(default=False)
    name = models.CharField(max_length=50, default='waiter1')
    seating = models.ManyToManyField(Seating)

    def __str__(self):
        return "%s: %s" % (self.name, "on duty" if self.onduty else "off duty")

    def set_waiter_on_duty(self):
        """Set the waiter to be on duty."""
        self.onduty = True
        self.save()
        print("waiter %s is on duty" % self.name)

    def set_waiter_off_duty(self):
        """Set the waiter to be off duty."""
        self.onduty = False
        self.save()
        print("waiter %s is off duty" % self.name)


class OrderItem(models.Model):
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return "%s %s" % (self.quantity, self.menu_item)

    def get_price(self):
        """Return the total price of this item."""
        return self.menu_item.price * self.quantity

    def reduce_item_stock(self):
        """Reduce the stock count of the menu item by quantity."""
        self.menu_item.stock -= self.quantity
        self.menu_item.save()

    def refund_item_stock(self):
        """Increase the stock count of the menu item by quantity."""
        self.menu_item.stock += self.quantity
        self.menu_item.save()


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

class Payment(models.Model):

    card_holder = models.CharField(max_length=50, default='na')     # name of card holder
    card_number = models.CharField(max_length=16, default='na')     # Card number
    cvc = models.CharField(max_length=3, default='na')              # CVC
    expiry = models.CharField(max_length=5, default='na')           # Card expiry date
    terms_conditions = models.BooleanField(default=False)           # Customer has accepted t and c
    payment_requested = models.BooleanField(default=False)          # Waiter has asked for payment
    payment_received = models.BooleanField(default=False)           # Payment information has been received
    payment_accepted = models.BooleanField(default=False)           # Waiter has accepted the payment

    def __str__(self):
       return "Order: %s, Accepted: %s" % (self.id, self.payment_accepted)

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

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)  # order of payment
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
    paid = models.BooleanField(default=False)  # order has been paid

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
        # pastOrder collects total of previos order and adds to current order.
        pastOrder = Order.objects.filter(table= seating_id)
        for ord in pastOrder:
            total_price += ord.total_price  # when reading total order look at the last order customer made

        order = Order.objects.create(
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

        # handle an OrderExtra if it exists
        try:
            order_extra = OrderExtra.active_objects.get(seating=Seating.objects.get(pk=seating_id))
            for order_item in order_extra.items.all():
                order.items.add(order_item)
            order_extra.used = True
            order_extra.save()
            order.total_price += sum([item.get_price() for item in order_extra.items.all()])
            order.save()
        except:
            pass

        order.save()
        return order

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

    def reduce_stock(self):
        for order_item in self.items.all():
            order_item.reduce_item_stock()

    def refund_stock(self):
        for order_item in self.items.all():
            order_item.refund_item_stock()


class ActiveOrderExtraManager(models.Manager):
    """Filter for active (unused) OrderExtras."""
    def get_queryset(self):
        return super().get_queryset().filter(used=False)


class UsedTodayOrderExtraManager(models.Manager):
    """Filter for today's used OrderExtras."""
    def get_queryset(self):
        return super().get_queryset().filter(used=True).filter(time__date=date.today())


class UsedWeekOrderExtraManager(models.Manager):
    """Filter for this week's used OrderExtras."""
    def get_queryset(self):
        return super().get_queryset().filter(used=True).filter(
            time__date__gt=timezone.now().date()-timedelta(days=7)
        )


class OrderExtra(models.Model):
    objects = models.Manager()
    active_objects = ActiveOrderExtraManager()
    used_today_objects = UsedTodayOrderExtraManager()
    used_week_objects = UsedWeekOrderExtraManager()

    seating = models.ForeignKey(Seating, on_delete=models.CASCADE)
    waiter = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    used = models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "OrderExtra #%s: %s, waiter: %s, status: %s" % \
            (self.id, self.seating, self.waiter, "inactive" if self.used else "active")

    def add_item(self, menu_item_id, quantity):
        for item in self.items.all():
            if item.menu_item.id == menu_item_id:
                item.quantity += quantity
                item.save()
                return
        self.items.add(OrderItem.objects.create(
            menu_item=Menu.objects.get(pk=menu_item_id),
            quantity=quantity,
        ))

    def get_total(self):
        return sum([order_item.get_price() for order_item in self.items.all()])
