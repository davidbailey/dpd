import unittest

from astropy import units

from dpd.mechanics import Bicycle


class TestBicycle(unittest.TestCase):
    def test_bicycle(self):
        truck = Bicycle(
            x=0,
            y=0,
            theta=0,
            velocity=1,
            acceleration=0,
            vehicle_length=29.5 * units.imperial.foot,
        )
        radius = truck.get_radius_from_vehicle_length_and_steering_angle(
            steering_angle=35 * units.degree
        )

        self.assertEqual(radius, 42.20804673074035 * units.imperial.foot)


if __name__ == "__main__":
    unittest.main()
