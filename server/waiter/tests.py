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

    def test_get_confirmed(self):
        """Orders that are unconfirmed"""
        test_order = Order.objects.get(pk=100)
        self.assertEqual(test_order.confirmed, False)