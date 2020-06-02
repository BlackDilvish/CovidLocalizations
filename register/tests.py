from django.test import TestCase, Client

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_get(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_empty_post(self):
        response = self.client.post(path='/register/', data={'username':'', 'password':''})

        self.assertIn(b'This field is required.', response.content)
        self.assertEqual(response.status_code, 200)

    def test_loggedout(self):
        response = self.client.post(path='/register/loggedout') 

        self.assertIn(b'You\'ve been logged out', response.content)
        self.assertEqual(response.status_code, 200)

