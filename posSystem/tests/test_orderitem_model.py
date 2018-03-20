from django.test import TestCase
from core.models import Menu, OrderItem


class TestOrderItemModel(TestCase):
    def setUp(self):
        menu_item = Menu.objects.create(
            price=10.00,
            stock=15,
        )
        OrderItem.objects.create(
            pk=0,
            menu_item=menu_item,
            quantity=5,
        )

    def test_get_price(self):
        order_item = OrderItem.objects.get(pk=0)
        self.assertEqual(order_item.get_price(), 50.0)

    def test_recude_item_stock(self):
        order_item = OrderItem.objects.get(pk=0)
        self.assertEqual(order_item.menu_item.stock, 15)
        order_item.reduce_item_stock()
        self.assertEqual(order_item.menu_item.stock, 10)

    def test_refund_item_stock(self):
        order_item = OrderItem.objects.get(pk=0)
        self.assertEqual(order_item.menu_item.stock, 15)
        order_item.refund_item_stock()
        self.assertEqual(order_item.menu_item.stock, 20)
