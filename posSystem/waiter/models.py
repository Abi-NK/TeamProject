from django.db import models
import json
from customer.models import Menu, Seating
from django.utils import timezone
from datetime import datetime, timedelta, date


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


class Order(models.Model):

    objects = models.Manager()
    active_objects = ActiveOrderManager()
    confirmed_objects = ConfirmedOrderManager()
    unconfirmed_objects = UnconfirmedOrderManager()
    ready_objects = ReadyOrderManager()
    delivered_today_objects = DeliveredTodayOrderManager()
    delivered_week_objects = DeliveredWeekOrderManager()

    table = models.CharField(max_length=100, default='na')
    time = models.DateTimeField()  # The time at which the order was taken
    items = models.CharField(max_length=1000, default='na')  # Includes prices as plaintext
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
            table=Seating.objects.get(pk=request.session["seating_id"]).label,
            confirmed=False,
            time=timezone.now(),
            items="\n".join(["%s %s" % (order_json[str(item.id)], str(item)) for item in order_contents]),
            cooking_instructions='none',
            purchase_method='none',
            total_price=total_price,
            delivered=False,
        ).save(force_insert=True)

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
