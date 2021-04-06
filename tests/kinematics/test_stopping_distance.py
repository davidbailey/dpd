import unittest

from astropy import units

from dpd.kinematics import stopping_distance

DECELERATION = - 6 * units.meter / (units.second * units.second)
INITIAL_VELOCITY = 60 * units.imperial.mile / units.hour
FINAL_VELOCITY = 0 * units.imperial.mile / units.hour

RESULT = 59.95342848


class TestStoppingDistance(unittest.TestCase):
    def test_stopping_distance(self):
        result = stopping_distance(DECELERATION, INITIAL_VELOCITY, FINAL_VELOCITY)
        self.assertEqual(RESULT, result.to_value(units.meter))


if __name__ == "__main__":
    unittest.main()
