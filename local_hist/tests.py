from django.test import TestCase
from . import views

class LocalHistTestCase(TestCase):
    def setUp(self):
        pass

    def test_prepare_waypoints(self):
        points = [[0,0],[100,100]]
        self.assertEqual(views.prepare_waypoints([], [0,0], [100,100]), points)
    