from django.test import TestCase
from core.models import Menu


class TestMenuModel(TestCase):
    def setUp(self):
        for i in range(10):
            Menu.objects.create(
                pk=i,
                name="Test item %s" % i,
                price=10.00,
                description="",
                course="",
                category="",
                stock=20,
            )

    def test_stock_manager(self):
        test_json = {}
        for i in range(10):
            test_json[str(i)] = i
        Menu.stock_manager.reduce_stock(test_json)
        for i in range(10):
            stock = Menu.objects.get(pk=i).stock
            self.assertEqual(stock, 20-i)
