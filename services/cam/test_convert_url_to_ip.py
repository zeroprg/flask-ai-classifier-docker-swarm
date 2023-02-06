import unittest
from video_streams import convert_url_to_ip

class TestConvertUrlToIp(unittest.TestCase):
    def test_valid_url(self):
        url = "https://csea-me-webcam.cse.umn.edu/mjpg/video.mjpg?timestamp=1443034719346"
        result = convert_url_to_ip(url)
        print(f"IP address {result}")
        self.assertIsNotNone(result)

    def test_invalid_url(self):
        url = "invalid.url"
        result = convert_url_to_ip(url)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
