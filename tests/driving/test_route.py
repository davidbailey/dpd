import unittest

from dpd.driving import Route
from dpd.osm import OSM


relation = 2351006
osm = OSM()
osm.download_relation(relation)


class TestRoute(unittest.TestCase):
    def test_route(self):
        self.route = Route.from_osm_relation(osm, relation)


if __name__ == "__main__":
    unittest.main()
