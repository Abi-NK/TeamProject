from django.test import TestCase
from waiter.models import Order
from django.utils import timezone
from kitchen.views import readyDelivery


class TestMakingDelivery(TestCase):

    def setUp(self):
        Order.objects.create(pk=666,
                             table="Test Table",
                             items="Test item 1",
                             time=timezone.now(),
                             cooking_instructions="none",
                             purchase_method="none",
                             total_price=66.60,
                             confirmed=False,
                             ready_delivery=False,
                             delivered=False)

    def test_ready_delivery(self):
        """Orders that are ready for delivery"""
        test_order = Order.objects.get(pk=666)
        #readyDelivery(str(test_order.id))
        self.assertEqual(readyDelivery(str(test_order.id)), True)
