from django.test import TestCase
from .models import Seating


# Create your tests here.
class TestSeatingModel(TestCase):
    def setUp(self):
        for i in range(1, 6):
            Seating.objects.create(label=("Table " + str(i)))

    def test_available_seating_manager(self):
        self.assertEqual(Seating.available_objects.count(), 5)
        Seating.objects.get(label="Table 1").set_unavailable()
        Seating.objects.get(label="Table 3").set_unavailable()
        Seating.objects.get(label="Table 4").set_unavailable()
        self.assertEqual(Seating.available_objects.count(), 2)

    def test_set_availability(self):
        seating = Seating.objects.get(label="Table 1")
        self.assertIs(seating.available, True)
        seating.set_unavailable()
        self.assertIs(seating.available, False)
