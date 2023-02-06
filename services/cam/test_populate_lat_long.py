import unittest
import mock

from video_streams import populate_lat_long

class TestPopulateLatLong(unittest.TestCase):
    def test_populate_lat_long(self):
        params = {
            'url': 'www.google.com'
        }
        # Here we will mock the get_geolocation_by_ip and convert_url_to_ip functions 
        # so that the test is only focused on the populate_lat_long function.
        def mock_get_geolocation_by_ip(ip):
            return {             
                "ipAddress": "8.8.8.8",
                'location': {
                    "city": "Mountain View",
                    "region": "California",
                    "regionCode": "CA",
                    "country": "US",
                    "continentCode": "NA",
                    'lat': 37.4192,
                    'lng': -122.0574,
                    'city': 'Mountain View',
                    'postalCode': '94043',
                    'country': 'United States'
                }    
            }    
        
        def mock_convert_url_to_ip(url):
            return '8.8.8.8'

        with mock.patch('video_streams.get_geolocation_by_ip', mock_get_geolocation_by_ip):
            with mock.patch('video_streams.convert_url_to_ip', mock_convert_url_to_ip):
                populate_lat_long(params)
                self.assertEqual(params['lat'], 37.4192)
                self.assertEqual(params['lng'], -122.0574)
                self.assertEqual(params['city'], 'Mountain View')
                self.assertEqual(params['postalcode'], '94043')
                self.assertEqual(params['country'], 'United States')

if __name__ == '__main__':
    unittest.main()
