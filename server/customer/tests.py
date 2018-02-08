from django.test import TestCase
from .models import Seating


# Create your tests here.
class TestSeatingModel(TestCase):
    def setUp(self):
        for i in range(1, 6):
            Seating.objects.create(label=("Table " + str(i)))

    def test_set_availability(self):
        seating = Seating.objects.all()[0]
        self.assertIs(seating.available, True)
        seating.set_unavailable()
        self.assertIs(seating.available, False)
