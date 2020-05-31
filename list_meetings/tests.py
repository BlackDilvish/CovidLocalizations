from django.test import TestCase
from . import views
import copy

class ListMeetingsTestCase(TestCase):
    def setUp(self):
        self.contact = {
            'distance': '50.55',
            'location': {
                'latitudeE7': 503282203,
                'longitudeE7': 192263489,
            }
        }

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


    
