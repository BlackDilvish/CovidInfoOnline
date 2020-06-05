from django.test import TestCase, Client
from . import views

class HeatmapTestCase(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_heatmap_get(self):
        response = self.client.get('/heatmap/')
        self.assertEqual(response.status_code, 200)
    
    def test_heatmap_empty_post(self):
        response = self.client.post(path = '/heatmap/', data = {'choose_month': '', 'choose_year': ''})
        self.assertEqual(response.status_code, 200)

    def test_heatmap_nonempty_post(self):
        response = self.client.post(path = '/heatmap/', data = {'choose_month': 'June', 'choose_year': '2020'})
        self.assertEqual(response.status_code, 200)
    
    def test_get_user_coordinates(self):
        points = {'data': { 'timelineObjects': [] }}
        points['data']['timelineObjects'].append({"activitySegment" : {
                        "startLocation" : { "latitudeE7" : 0, "longitudeE7" : 50000000 },
                        "endLocation" : { "latitudeE7" : 10000000, "longitudeE7" : 20000000}
                    }})

        points['data']['timelineObjects'].append({"placeVisit" : {
                        "location" : { "latitudeE7" : 30000000, "longitudeE7" : 40000000 }
                    }})

        self.assertEqual(views.get_user_coordinates([points]), [[1,2], [0,5], [3,4]])
    
    def test_get_contacts_coordinates(self):
        points = { "location" : { "latitudeE7" : 0, "longitudeE7" : 50000000}}

        self.assertEqual(views.get_contacts_coordinates([points]), [[0,5]])
    
    def test_get_user_and_contacts_coordinates(self):
        self.assertEqual(views.get_user_and_contacts_coordinates([10,10], [20,20]), [])
