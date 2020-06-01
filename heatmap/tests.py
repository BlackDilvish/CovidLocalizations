from django.test import TestCase
from . import views

class HeatmapTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_user_coordinates(self):
        self.assertEqual(views.get_user_coordinates([]), [])

    def test_get_contacts_coordinates(self):
        self.assertEqual(views.get_contacts_coordinates([]), [])
    
    def test_get_user_and_contacts_coordinates(self):
        self.assertEqual(views.get_user_and_contacts_coordinates([], []), [])
