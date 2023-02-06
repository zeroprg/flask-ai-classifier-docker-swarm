import unittest
import requests_mock
import io

import unittest.mock

from video_streams import get_geolocation_by_ip

class TestGetGeolocationByIP(unittest.TestCase):
    def setUp(self):
        self.ip = "8.8.8.8"
        self.url = "https://whoisapi-ip-geolocation-v1.p.rapidapi.com/api/v1?ipAddress={}".format(self.ip)
        self.expected_response = {
            "status": "success",
            "message": "",
            "data": {
                "ipAddress": "8.8.8.8",
                "city": "Mountain View",
                "region": "California",
                "regionCode": "CA",
                "country": "United States",
                "countryCode": "US",
                "continent": "North America",
                "continentCode": "NA"
            }
        }

    @requests_mock.Mocker()
    def test_get_geolocation_by_ip_success(self, mocker):
        mocker.get(self.url, json=self.expected_response)

        with unittest.mock.patch("builtins.open", unittest.mock.mock_open(read_data="ip_geolocation=api_key")):
            with unittest.mock.patch("sys.stdout", new_callable=io.StringIO) as stdout:
                result = get_geolocation_by_ip(self.ip)
                self.assertEqual(result, self.expected_response)

    @requests_mock.Mocker()
    def test_get_geolocation_by_ip_failure(self, mocker):
        mocker.get(self.url, status_code=400)

        with unittest.mock.patch("builtins.open", unittest.mock.mock_open(read_data="ip_geolocation=api_key")):
            with unittest.mock.patch("sys.stdout", new_callable=io.StringIO) as stdout:
                result = get_geolocation_by_ip(self.ip)
                self.assertIsNone(result)
                self.assertIn("HTTP error occurred", stdout.getvalue().strip())

if __name__ == '__main__':
    unittest.main()
