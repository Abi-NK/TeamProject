from django.test import TestCase
from core.models import Menu
from core.views import menu_views
from manager.forms import AdjustMenuForm
from django.test import RequestFactory


class ManagerFormTest(TestCase):

    # Set up test
    def setUp(self):
        self.menu = Menu.objects.create(id=100, name="taco", price=10, description="nice good food", course="main",
                                        category="tacos", allergy="uyhg", calories=99, image="imgur.com/sef32",
                                        vegetarian=False, vegan=False, meat=False, stock=5, cost=10)
        self.factory = RequestFactory()

    # Test 1
    def test_get_remove_menu_item_request(self):
        """Test initial get request is valid"""
        request = self.factory.get('')
        response = menu_views.remove_menu_item(request)
        self.assertEqual(response.status_code, 405)

    # Test 2
    def test_get_adjust_menu_request(self):
        """Test initial get request for managermenu.html is valid"""
        request = self.factory.get('/manager/managermenu')
        response = menu_views.adjust_menu(request)
        self.assertEqual(response.status_code, 200)

    # Test 3
    def test_form_valid(self):
        """Test form validation is valid"""
        form = AdjustMenuForm(data={'id': 100, 'name': "taco", 'price': 10, 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': 5, 'cost': 10})

        self.assertTrue(form.is_valid())

    # Test 4
    def test_form_invalid_negative_stock(self):
        """Test an invalid form with negative stock"""
        form = AdjustMenuForm(data={'id': 100, 'name': "taco", 'price': 10, 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': -5, 'cost': 10})

        self.assertFalse(form.is_valid())

    # Test 5
    def test_form_invalid_decimal_price(self):
        """Test an invalid form with a decimal with three decimal places"""
        form = AdjustMenuForm(data={'id': 100, 'name': "taco", 'price': 10.555, 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': 5, 'cost': 10})

        self.assertFalse(form.is_valid())

    # Test 6
    def test_form_invalid_string_price(self):
        """Test an invalid form with a string as the price"""
        form = AdjustMenuForm(data={'id': 100, 'name': "taco", 'price': "wrong", 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': 5, 'cost': 10})

        self.assertFalse(form.is_valid())

    # Test 7
    def test_form_invalid_long_name(self):
        """Test an invalid form with a name that's over the character count"""
        form = AdjustMenuForm(data={'id': 100, 'name': "a"*10000, 'price': 10, 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': 5, 'cost': 10})

        self.assertFalse(form.is_valid())

    # Test 8
    def test_form_valid_reduced_price(self):
        """Test valid form with a valid reduced price"""
        form = AdjustMenuForm(data={'id': 100, 'name': "taco", 'price': 6, 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': 5, 'cost': 10})

        self.assertTrue(form.is_valid())

    # Test 9
    def test_form_invalid_cost_too_large(self):
        """Test invalid form with a cost that is too large"""
        form = AdjustMenuForm(data={'id': 100, 'name': "taco", 'price': 6, 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': 5, 'cost': 100*10000000000000000000000})

        self.assertFalse(form.is_valid())
