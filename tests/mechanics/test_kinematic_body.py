import unittest

from astropy import units

from dpd.mechanics import KinematicBody


class TestKinematicBody(unittest.TestCase):
    def test_kinematic_body(self):
        kinematic_body = KinematicBody(initial_velocity=1 * units.meter / units.second)
        next_time, next_distance = kinematic_body.step()
        self.assertEqual(next_time, 1 * units.second)
        self.assertEqual(next_distance, 1 * units.meter)


if __name__ == "__main__":
    unittest.main()
