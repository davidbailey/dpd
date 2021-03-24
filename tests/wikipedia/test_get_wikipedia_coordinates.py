import unittest

from dpd.wikipedia import get_wikipedia_coordinates


class TestGetWikipediaCoordinates(unittest.TestCase):
    def test_get_wikipedia_coordinates(self):
        new_york_city = get_wikipedia_coordinates(
            "https://en.wikipedia.org/wiki/New_York_City"
        )
        self.assertEqual(new_york_city, ('40°42′46″N', '74°00′22″W'))


if __name__ == "__main__":
    unittest.main()
