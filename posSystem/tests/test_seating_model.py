from django.test import TestCase
from core.models import Seating


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

    def test_occupied_seating_manager(self):
        self.assertEqual(Seating.occupied_objects.count(), 0)
        Seating.objects.get(label="Table 1").set_unavailable()
        Seating.objects.get(label="Table 3").set_unavailable()
        Seating.objects.get(label="Table 4").set_unavailable()
        self.assertEqual(Seating.occupied_objects.count(), 3)

    def test_set_unavailable(self):
        seating = Seating.objects.get(label="Table 1")
        self.assertIs(seating.available, True)
        seating.set_unavailable()
        self.assertIs(seating.available, False)

    def test_set_available(self):
        seating = Seating.objects.get(label="Table 1")
        seating.set_unavailable()
        self.assertIs(seating.available, False)
        seating.set_available()
        self.assertIs(seating.available, True)

    def test_set_assistance_true(self):
        seating = Seating.objects.get(label="Table 1")
        self.assertIs(seating.assistance, False)
        seating.set_assistance_true()
        self.assertIs(seating.assistance, True)

    def test_set_assistance_false(self):
        seating = Seating.objects.get(label="Table 1")
        seating.set_assistance_true()
        self.assertIs(seating.assistance, True)
        seating.set_assistance_false()
        self.assertIs(seating.assistance, False)
