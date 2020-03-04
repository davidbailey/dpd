import unittest

from dpd.gtfs import url2gtfs, get_stops_by_route_type

class TestGTFS(unittest.TestCase):
    def test_gtfs(self):
        self.feed = url2gtfs("http://iportal.sacrt.com/gtfs/SRTD/google_transit.zip")
        self.assertEqual(feed.agency["agency_id"][0], 'SRTD')
        self.type_zero_stops = get_stops_by_route_type(self.feed, 0)
        self.assertEqual(len(self.type_zero_stops), 102)


if __name__ == "__main__":
    unittest.main()
