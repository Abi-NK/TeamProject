from django.test import TestCase
from customer.models import Menu
from manager.forms import AdjustMenuForm


class ManagerFormTest(TestCase):

    def setUp(self):
        self.menu = Menu.objects.create(id=100, name="taco", price=10, description="nice good food", course="main",
                                        category="tacos", allergy="uyhg", calories=99, image="imgur.com/sef32",
                                        vegetarian=False, vegan=False, meat=False, stock=5)

    def test_form_valid(self):
        form = AdjustMenuForm(data={'id': 100, 'name': "taco", 'price': 10, 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': 5})

        self.assertTrue(form.is_valid())

    def test_form_invalid_negative_stock(self):
        form = AdjustMenuForm(data={'id': 100, 'name': "taco", 'price': 10, 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': -5})

        self.assertFalse(form.is_valid())

    def test_form_invalid_decimal_price(self):
        form = AdjustMenuForm(data={'id': 100, 'name': "taco", 'price': 10.555, 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': 5})

        self.assertFalse(form.is_valid())

    def test_form_invalid_string_price(self):
        form = AdjustMenuForm(data={'id': 100, 'name': "taco", 'price': "wrong", 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': 5})

        self.assertFalse(form.is_valid())

    def test_form_invalid_long_name(self):
        form = AdjustMenuForm(data={'id': 100, 'name': "a"*10000, 'price': 10, 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': 5})

        self.assertFalse(form.is_valid())

    def test_form_valid_reduced_price(self):
        form = AdjustMenuForm(data={'id': 100, 'name': "taco", 'price': 6, 'description': "nice good food",
                                    'course': "main", 'category': "tacos", 'allergy': "uyhg", 'calories': 99,
                                    'image': "imgur.com/sef32", 'vegetarian': False, 'vegan': False, 'meat': False,
                                    'stock': 5})

        self.assertTrue(form.is_valid())
