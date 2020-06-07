from django.test import TestCase, Client
from datetime import date
from . import views
from . import models

class LocalizatorTestViews(TestCase):
    def setUp(self):
        self.client = Client()

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

    def test_index(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)


class LocalizatorTestModels(TestCase):
    def setUp(self):
        pass

    def test_localizations_data(self):
        loc_data = models.LocalizationsData()

        loc_data.name = 'name'
        loc_data.file_date = '01.01.2020'

        self.assertEqual(str(loc_data), 'name')
        self.assertEqual(loc_data.date(), str(date.today()))
        self.assertEqual(loc_data.json_file_date(), '01.01.2020')

    def test_health_status(self):
        health = models.HealthStatus()

        health.name = 'name'
        health.status = True
        health.start_date = date.today()
        health.end_date = date.today()

        self.assertEqual(str(health), 'name')
        self.assertEqual(health.covid_status(), True)
        self.assertEqual(health.covid_start_date(), str(date.today()))
        self.assertEqual(health.covid_end_date(), str(date.today()))

