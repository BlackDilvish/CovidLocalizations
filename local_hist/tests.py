from django.test import TestCase, Client
from . import views
from datetime import datetime
from django.urls import reverse

class LocalHistTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_local_hist_post(self):
        response = self.client.post(path = '/local_hist/', data = {'choose_month': 'January', 'choose_year': '2019'})
        self.assertEqual(response.status_code, 200) 
            
    def test_local_hist_empty_post(self):
        response = self.client.post(path = '/local_hist/', data = {'choose_month': '', 'choose_year': ''})
        self.assertEqual(response.status_code, 200)
       	
    def test_local_hist_get(self):
        response = self.client.get('/local_hist/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'local_hist/local_hist.html') 
        
    def test_visit(self):
        url = reverse('visit', args = [20, 50])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'local_hist/local_map.html')  
        
    def test_activity(self):
        url = reverse('activity', args = [20, 50, 20, 50])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'local_hist/local_map.html')       
	
    def test_prepare_waypoints(self):
        points = [[0,0], [5,5], [7,7], [10,10]] 
        waypoints = [{"latE7": 50000000, "lngE7": 50000000}, {"latE7": 70000000, "lngE7": 70000000}]
        self.assertEqual(views.prepare_waypoints(waypoints, [0,0], [10,10]), points)
    
    def test_item_activity(self):
        item = TestItem()
        self.assertEqual(len(views.item_activity(item, 0)), 2)
        
    def test_item_visit(self):
        item = TestItem()
        item.data = {"timelineObjects": [{"placeVisit": {"location": {"longitudeE7": 7654321}}}]}
        vis = views.item_visit(item, 0)
        lon = item.data["timelineObjects"][0]["placeVisit"]["location"]["longitudeE7"]
        self.assertEqual(vis["Places_longitude"], lon)
    
    def test_convert_time(self):
        output = []
        item = TestItem()
        output.append(views.item_activity(item, 0))
        output = views.convert(output)
        self.assertEqual(output[0]["End_time"], datetime(2020, 6, 2, 12, 11, 25))
       
    def test_convert_location(self):
        output = []
        item = TestItem()
        item.data = {"timelineObjects": [{"placeVisit": {"location": {"longitudeE7": 123456789}}}]} 
        output.append(views.item_visit(item, 0))
        output = views.convert(output)
        self.assertEqual(output[0]["Places_longitude"], 12.346)
     
class TestItem():
    data = {"timelineObjects": [{"activitySegment": {"duration": {"endTimestampMs": "1591099885000"}}}]}
    
