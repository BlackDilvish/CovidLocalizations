from django.test import TestCase, Client
from datetime import date
import os
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

    def test_get_error_format(self):
        self.assertEqual(views.get_error_format(), 
                        'It seems that your file is valid JSON, but it does not contain required content')

    def test_get_error_date(self):
        self.assertEqual(views.get_error_date(), 
                        'Selected dates are incorrect!')

    def test_check_for_label(self):
        self.assertEqual(views.check_for_label('nolabel'), False)

    def test_check_status_dates(self):
        self.assertEqual(views.check_status_dates(date.today(), date.today()), True)

    def test_get_mail_title(self):
        status = '[COVID LOCALIZATIONS] Important! Possible contact with infected person occured.' in views.get_mail_title()
        self.assertEqual(status, True)

    def test_home(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_upload_get(self):
        response = self.client.get('/upload')
        self.assertEqual(response.status_code, 200)

    def test_upload_post(self):
        response = self.client.post(path='/upload', data={'file': ''})
        self.assertEqual(response.status_code, 200)

    def test_status_get(self):
        response = self.client.get('/status')
        self.assertEqual(response.status_code, 200)

    def test_status_post(self):
        response = self.client.post(path='/status', data={})
        self.assertEqual(response.status_code, 200)

    def test_instruction(self):
        response = self.client.get('/instruction')
        self.assertEqual(response.status_code, 200)

    def test_convert_date(self):
        converted = views.convert_date('')
        self.assertEqual(converted, date.today())

    def test_validate_json(self):
        with open('test.json', 'w+') as f:
            f.write('{"key": 0}')
            validated = views.validate_json(f)

        os.remove('test.json')
        
        self.assertEqual(validated, False)


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

