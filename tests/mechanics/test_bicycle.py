import unittest

from astropy import units

from dpd.mechanics import Bicycle


class TestBicycle(unittest.TestCase):
    def test_bicycle(self):
        truck = Bicycle(
            x=0 * units.meter,
            y=0 * units.meter,
            theta=0 * units.degree,
            velocity=1 * units.meter / units.second,
            acceleration=0 * units.meter / units.second**2,
            vehicle_length=29.5 * units.imperial.foot,
        )
        radius = truck.get_radius_from_vehicle_length_and_steering_angle(
            steering_angle=35 * units.degree
        )

        self.assertEqual(radius, 42.1303662 * units.imperial.foot)


if __name__ == "__main__":
    unittest.main()
