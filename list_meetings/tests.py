from django.test import TestCase, Client
from . import views
import copy

class ListMeetingsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact = {
            'distance': 50.55,
            'location': {
                'latitudeE7': 503282203,
                'longitudeE7': 192263489,
            }
        }

    def test_clear_contacts(self):
        contacts = [self.contact]
        contacts[0].pop('distance')
        views.clear_contacts(contacts)
        self.assertEqual(contacts, [])
    
    def test_get_contacts(self):
        self.assertEqual(views.get_contacts('test', 'June2021'), [])
    
    def test_prepare_contacts(self):
        self.assertEqual(views.prepare_contacts([self.contact], 'testowy', 'June2021'), True)

    def test_by_distance(self):
        self.assertEqual(views.by_distance(self.contact), 50.55)

    def test_map_contacts_locations(self):
        test_contact = copy.deepcopy(self.contact)

        views.map_contacts_locations([test_contact])

        self.assertEqual(test_contact['location']['latitude'], 
                        str(round(float(self.contact['location']['latitudeE7'] / views.divider), 
                            views.precision)))

        self.assertEqual(test_contact['location']['longitude'], 
                        str(round(float(self.contact['location']['longitudeE7'] / views.divider),
                            views.precision)))