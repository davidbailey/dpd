import unittest

from dpd.driving import Route, Vehicle
from dpd.osm import OSM


relation = 2351006
osm = OSM()
osm.download_relation(relation)


class TestRoute(unittest.TestCase):
    def test_route(self):
        self.vehicle = Vehicle(24.5872, 0.5, -0.5)
        self.route = Route.from_osm_relation(osm, relation)
        self.trip = self.route.drive(self.vehicle, 45)


if __name__ == "__main__":
    unittest.main()
