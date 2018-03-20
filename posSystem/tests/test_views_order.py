from django.test import TestCase
from core.models import Order, Menu
from core.views import order_views
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth import authenticate


class OrderTest(TestCase):

    # Set up test
    def setUp(self ):
        self.menu = Menu.objects.create(id=100, name="taco", price=10, description="nice good food", course="main",
                                        category="tacos", allergy="uyhg", calories=99, image="imgur.com/sef32",
                                        vegetarian=False, vegan=False, meat=False, stock=5)
        self.factory = RequestFactory()

        self.credentials = {
            'username': 'waiter1',
            'password': 'password'}
        User.objects.create_user(**self.credentials)


    # Test 1
    def test_login(self):
        """Test login for this view"""
        self.c = Client()
        self.user = User.objects.create(username='testuser', password='12345')
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser', password='hello')
        login = self.c.login(username='testuser', password='hello')
        self.assertTrue(login)
