from django.test import TestCase
from .models import Order
from django.utils import timezone
import unittest


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

