from django.test import TestCase
from core.models import Menu, OrderExtra, Seating
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class TestOrderExtraModel(TestCase):
    def setUp(self):
        waiter = User.objects.create_user(
            username="waiter1",
        )
        seating = Seating.objects.create(
            pk=0,
            label="Test Seating 1",
        )
        OrderExtra.objects.create(
            pk=0,
            seating=seating,
            waiter=waiter,
        )
        Menu.objects.create(pk=0, price=5.00)
        Menu.objects.create(pk=1, price=10.00)
        Menu.objects.create(pk=2, price=15.00)

    def test_add_item(self):
        order_extra = OrderExtra.objects.get(pk=0)
        order_extra.add_item(0, 3)
        order_extra.add_item(1, 4)
        order_extra.add_item(2, 5)
        order_extra.add_item(2, 5)
        order_extra.add_item(2, 5)
        self.assertEqual(sum([item.quantity for item in order_extra.items.all()]), 22)

    def test_get_total(self):
        order_extra = OrderExtra.objects.get(pk=0)
        self.assertEqual(order_extra.get_total(), 0)
        order_extra.add_item(0, 1)
        order_extra.add_item(1, 2)
        order_extra.add_item(2, 3)
        self.assertEqual(order_extra.get_total(), 70)

    def test_active_order_extra_manager(self):
        order_extra = OrderExtra.objects.get(pk=0)
        self.assertEqual(OrderExtra.active_objects.count(), 1)
        order_extra.used = True
        order_extra.save()
        self.assertEqual(OrderExtra.active_objects.count(), 0)

    def test_used_today_order_extra_manager(self):
        order_extra = OrderExtra.objects.get(pk=0)
        self.assertEqual(OrderExtra.used_today_objects.count(), 0)
        order_extra.used = True
        order_extra.save()
        self.assertEqual(OrderExtra.used_today_objects.count(), 1)
        waiter = User.objects.create_user(username="waiterTest")
        seating = Seating.objects.create()
        OrderExtra.objects.create(
            waiter=waiter,
            seating=seating,
            time=timezone.now() - timedelta(days=1),
            used=True,
        )
        self.assertEqual(OrderExtra.used_today_objects.count(), 1)

    def test_used_week_order_extra_manager(self):
        waiter = User.objects.create_user(username="waiterTest")
        seating = Seating.objects.create()
        for i in range(10):
            OrderExtra.objects.create(
                waiter=waiter,
                seating=seating,
                time=timezone.now() - timedelta(days=i),
                used=True,
            )
        self.assertEqual(OrderExtra.used_week_objects.count(), 7)
