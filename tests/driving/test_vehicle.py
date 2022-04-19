import unittest

from astropy import units
from pandas import DataFrame

from dpd.driving import Vehicle


class TestVehicle(unittest.TestCase):
    def test_vehicle(self):
        segments = DataFrame(
            [
                (20 * units.meter / units.second, 1000 * units.meter),
                (5 * units.meter / units.second, 2000 * units.meter),
                (5 * units.meter / units.second, 3000 * units.meter),
                (100 * units.meter / units.second, 4000 * units.meter),
            ],
            columns=["speed_limit", "distance"],
        )
        vehicle = DynamicBody(
            power=75000 * 0.1 * units.watt,
            mass=2000 * units.kilogram,
            max_speed=150 * units.kilometer / units.hour,
            acceleration_limit=2 * units.meter / (units.second * units.second),
            max_deceleration=-1 * units.meter / (units.second * units.second),
        )
        drive = vehicle.drive_between_stops(
            segments.speed_limit.to_list(), segments.distance.to_list()
        )


if __name__ == "__main__":
    unittest.main()
