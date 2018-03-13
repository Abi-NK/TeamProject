from django.test import TestCase
from customer.models import Menu
from manager.forms import AdjustMenuForm


class ManagerFormTest(TestCase):

    def setUp(self):
        self.menu = Menu.objects.create(name="taco", price=3.55, description="nice good food", course="main",
                                        category="tacos", allergy="uyhg", calories=99, image="imgur.com/sef32",
                                        vegetarian=False, vegan=False, meat=False, stock=5)

    def test_form_valid(self):
        form = AdjustMenuForm(data={'name': "taco", 'price': 3.55, 'description': "nice good food", 'course': "main",
                                    'category': "tacos", 'allergy': "uyhg", 'calories': 99, 'image': "imgur.com/sef32",
                                    'vegetarian': False, 'vegan': False, 'meat': False, 'stock': 5})

        self.assertTrue(form.is_valid())

    def test_form_invalid_negative_stock(self):
        form = AdjustMenuForm(data={'name': "taco", 'price': 3.55, 'description': "nice good food", 'course': "main",
                                    'category': "tacos", 'allergy': "uyhg", 'calories': 99, 'image': "imgur.com/sef32",
                                    'vegetarian': False, 'vegan': False, 'meat': False, 'stock': -5})

        self.assertFalse(form.is_valid())

    def test_form_invalid_decimal_price(self):
        form = AdjustMenuForm(data={'name': "taco", 'price': 3.555, 'description': "nice good food", 'course': "main",
                                    'category': "tacos", 'allergy': "uyhg", 'calories': 99, 'image': "imgur.com/sef32",
                                    'vegetarian': False, 'vegan': False, 'meat': False, 'stock': 5})

        self.assertFalse(form.is_valid())

    def test_form_invalid_string_price(self):
        form = AdjustMenuForm(data={'name': "taco", 'price': "wrong", 'description': "nice good food", 'course': "main",
                                    'category': "tacos", 'allergy': "uyhg", 'calories': 99, 'image': "imgur.com/sef32",
                                    'vegetarian': False, 'vegan': False, 'meat': False, 'stock': 5})

        self.assertFalse(form.is_valid())

    def test_form_invalid_long_name(self):
        form = AdjustMenuForm(data={'name': "a"*10000,
                                    'price': 3.555, 'description': "nice good food", 'course': "main",
                                    'category': "tacos", 'allergy': "uyhg", 'calories': 99, 'image': "imgur.com/sef32",
                                    'vegetarian': False, 'vegan': False, 'meat': False, 'stock': 5})

        self.assertFalse(form.is_valid())
