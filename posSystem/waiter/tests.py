from django.test import TestCase
from .models import Order
from django.utils import timezone
from datetime import datetime, timedelta, date, time


class TestMarkingDelivery(TestCase):

    def setUp(self):
        Order.objects.create(pk=100,
                             table="Table 1",
                             items="Guacamole with tortilla chips",
                             time=timezone.now(),
                             cooking_instructions="none",
                             purchase_method="none",
                             total_price=13.20,
                             confirmed=False,
                             ready_delivery=False,
                             delivered=False)

        Order.objects.create(pk=200,
                             table="Table 1",
                             items="Guacamole with tortilla chips",
                             time=timezone.now(),
                             cooking_instructions="none",
                             purchase_method="none",
                             total_price=13.20,
                             confirmed=False,
                             ready_delivery=False,
                             delivered=False)

        Order.objects.create(pk=300,
                             table="Table 1",
                             items="Guacamole with tortilla chips",
                             time=timezone.now(),
                             cooking_instructions="none",
                             purchase_method="none",
                             total_price=13.20,
                             confirmed=False,
                             ready_delivery=False,
                             delivered=False)

        Order.objects.create(pk=400,
                             table="Table 1",
                             items="Guacamole with tortilla chips",
                             time=timezone.now(),
                             cooking_instructions="none",
                             purchase_method="none",
                             total_price=13.20,
                             confirmed=True,
                             ready_delivery=True,
                             delivered=False)

    def test_get_confirmed(self):
        """Orders that are unconfirmed"""
        test_order = Order.objects.get(pk=100)
        self.assertEqual(test_order.confirmed, False)

    def test_delivered(self):
        """"Order that has been delivered"""
        test_order = Order.objects.get(pk=100)
        self.assertEqual(test_order.delivered, False)
        test_order.set_delivered()
        self.assertEqual(test_order.delivered, True)

    def test_get_not_confirmed_orders(self):
        """"Get all non confirmed orders"""
        test_order = Order.objects.get(pk=200)
        self.assertEqual(test_order.confirmed, False)

    def test_set_confirmed(self):
        """"Order has been confirmed"""
        test_order = Order.objects.get(pk=300)
        self.assertEqual(test_order.confirmed, False)
        test_order.set_confirmed()
        self.assertEqual(test_order.confirmed, True)

    def test_set_ready_delivery(self):
        """"Order is ready for delivery"""
        test_order = Order.objects.get(pk=300)
        self.assertEqual(test_order.ready_delivery, False)
        test_order.set_ready_delivery()
        self.assertEqual(test_order.ready_delivery, True)

    def test_get_not_confirmed_orders_all(self):
        """"List of orders that are not confirmed, tests Orders with ID= 100, 200, 300 (defined above)"""
        test_order = Order.get_not_confirmed_orders(self)
        self.assertEqual(test_order[0].confirmed, False)
        self.assertEqual(test_order[1].confirmed, False)
        self.assertEqual(test_order[2].confirmed, False)

    def test_get_all_orders(self):
        test_order = Order.get_all_orders(self)
        self.assertEqual(test_order[0].id, 100)
        self.assertEqual(test_order[1].id, 200)
        self.assertEqual(test_order[2].id, 300)

    def test_get_kitchen_orders(self):
        test_order = Order.get_kitchen_orders(self)
        self.assertEqual(test_order[0].id, 400)

    def test_get_time_display(self):
        order = Order.objects.create(
            time=datetime.combine(date(2018, 1, 1), time(9, 30, 20)),
            total_price=0,
        )
        self.assertEqual(order.get_time_display(), "09:30:20")

    def test_get_price_display(self):
        order = Order.objects.create(
            time=timezone.now(),
            total_price=123.45,
        )
        self.assertEqual(order.get_price_display(), "£123.45")

    def test_is_nearly_late(self):
        self.assertFalse(Order.objects.get(pk=100).is_nearly_late())
        order = Order.objects.create(
            time=datetime.now() - timedelta(minutes=6),
            total_price=0,
        )
        self.assertFalse(order.is_nearly_late())
        order = Order.objects.create(
            time=datetime.now() - timedelta(minutes=8),
            total_price=0,
        )
        self.assertTrue(order.is_nearly_late())

    def test_is_late(self):
        self.assertFalse(Order.objects.get(pk=100).is_late())
        order = Order.objects.create(
            time=datetime.now() - timedelta(minutes=9),
            total_price=0,
        )
        self.assertFalse(order.is_late())
        order = Order.objects.create(
            time=datetime.now() - timedelta(minutes=11),
            total_price=0,
        )
        self.assertTrue(order.is_late())

    def test_active_order_manager(self):
        self.assertEqual(Order.active_objects.count(), 4)
        Order.objects.get(pk=100).set_delivered()
        Order.objects.get(pk=200).set_delivered()
        self.assertEqual(Order.active_objects.count(), 2)

    def test_confirmed_order_manager(self):
        self.assertEqual(Order.confirmed_objects.count(), 0)
        Order.objects.get(pk=100).set_confirmed()
        Order.objects.get(pk=200).set_confirmed()
        Order.objects.get(pk=300).set_confirmed()
        Order.objects.get(pk=300).set_ready_delivery()
        Order.objects.get(pk=400).set_confirmed()
        Order.objects.get(pk=400).set_ready_delivery()
        self.assertEqual(Order.confirmed_objects.count(), 2)

    def test_unconfirmed_order_manager(self):
        self.assertEqual(Order.unconfirmed_objects.count(), 3)
        Order.objects.get(pk=100).set_confirmed()
        Order.objects.get(pk=200).set_confirmed()
        Order.objects.get(pk=300).set_confirmed()
        self.assertEqual(Order.unconfirmed_objects.count(), 0)

    def test_ready_order_manager(self):
        self.assertEqual(Order.ready_objects.count(), 1)
        Order.objects.get(pk=100).set_ready_delivery()
        Order.objects.get(pk=200).set_ready_delivery()
        Order.objects.get(pk=200).set_delivered()
        self.assertEqual(Order.ready_objects.count(), 2)

    def test_delivered_today_manager(self):
        self.assertEqual(Order.delivered_today_objects.count(), 0)
        Order.objects.get(pk=100).set_delivered()
        Order.objects.get(pk=200).set_delivered()
        self.assertEqual(Order.delivered_today_objects.count(), 2)
