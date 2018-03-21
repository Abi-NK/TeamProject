from django.test import TestCase
from core.models import Menu
from django.test import RequestFactory


class TestMenuModel(TestCase):

    # Set up test
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

    # Test 1
    def test_stock_manager(self):
        test_json = {}
        for i in range(10):
            test_json[str(i)] = i
        Menu.stock_manager.reduce_stock(test_json)
        for i in range(10):
            stock = Menu.objects.get(pk=i).stock
            self.assertEqual(stock, 20-i)

    # Test 2
    def test_adding_menu_item(self):
        """Test adding an item to the Menu table"""
        Menu.objects.create(id=100, name="taco", price=10, description="nice good food", course="main",
                            category="tacos", allergy="uyhg", calories=99, image="imgur.com/sef32",
                            vegetarian=False, vegan=False, meat=False, stock=5)

        self.assertEqual(Menu.objects.all().count(), 11)

    # Test 3
    def test_removing_menu_item(self):
        """"Test removing an item from the Menu table"""
        Menu.objects.create(id=100, name="taco", price=10, description="nice good food", course="main",
                            category="tacos", allergy="uyhg", calories=99, image="imgur.com/sef32",
                            vegetarian=False, vegan=False, meat=False, stock=5)

        self.assertEqual(Menu.objects.all().count(), 11)

        Menu.objects.filter(pk=100).delete()

        self.assertEqual(Menu.objects.all().count(), 10)

    # Test 4
    def test_edit_menu_item(self):
        """Test editing an item in the Menu table"""
        Menu.objects.filter(pk=1).update(name="Pasta")
        name = Menu.objects.get(pk=1)
        self.assertEqual(name.name, "Pasta")
