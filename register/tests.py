from django.test import TestCase

class LoginTestCase(TestCase):
    def setUp(self):
        self.x = 2

    def test_2_eq_2(self):
        self.assertEqual(self.x, 2)

