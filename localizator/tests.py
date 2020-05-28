from django.test import TestCase
from . import views

class LocalizatorTest(TestCase):
    def setUp(self):
        pass

    def test_get_mail_address(self):
        self.assertEqual(views.get_mail_address(), 
                        'covid-localizations@no-reply.com')

    def test_get_no_html(self):
        self.assertEqual(views.get_no_html(), 
                        'There is a chance that you had close contacts (smaller than 250m) in following places: \n')

    def test_get_error_validation(self):
        self.assertEqual(views.get_error_validation(), 
                        'Unfortunately sent file is not valid json. Please, check your data.')

    def test_get_error_date(self):
        self.assertEqual(views.get_error_date(), 
                        'Selected dates are incorrect!')

    def test_check_for_label(self):
        self.assertEqual(views.check_for_label('nolabel'), False)
