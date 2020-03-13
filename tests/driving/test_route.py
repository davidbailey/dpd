import unittest

from dpd.driving import Route, Vehicle
from dpd.osm import OSM


relation = 2351006
osm = OSM()
osm.download_relation(relation)


class TestRoute(unittest.TestCase):
    def test_route(self):
        self.vehicle = Vehicle(24.5872, 1.3, -1.3, name="max_speed_55_mph_vehicle")
        self.route = Route.from_osm(osm, relation, tolerance=10)
        self.route.add_vehicle(self.vehicle)
        self.assertEqual(
            49.78333333333333,
            (
                self.route[self.route.stop_name != ""]["time_to_next_stop"].sum()
                + self.route.dwell_time.sum()
                - 45
            )
            / 60,
        )


if __name__ == "__main__":
    unittest.main()
