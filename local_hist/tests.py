from django.test import TestCase
from . import views

class LocalHistTestCase(TestCase):
    def setUp(self):
        pass

    def test_prepare_waypoints(self):
        points = [[0,0], [5,5], [7,7], [10,10]] 
        waypoints = [{"latE7": 50000000, "lngE7": 50000000}, {"latE7": 70000000, "lngE7": 70000000}]
        self.assertEqual(views.prepare_waypoints(waypoints, [0,0], [10,10]), points)
    