from django.db import models
from core.models import Menu, OrderItem, Seating
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date


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
