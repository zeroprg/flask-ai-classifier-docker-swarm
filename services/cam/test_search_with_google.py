import unittest
from video_streams import search_with_google

class TestSearchWithGoogle(unittest.TestCase):
    def test_search_with_google(self):
        # Test search with valid query and API key
        query = "test query"
        result = search_with_google(query)
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 0)
        for url in result:
            self.assertIsInstance(url, str)

if __name__ == '__main__':
    unittest.main()