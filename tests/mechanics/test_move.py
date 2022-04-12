import unittest

from astropy import units

from dpd.mechanics import move

ACCELERATION = 2.5 * units.meter / (units.second * units.second)
INITIAL_VELOCITY = 0 * units.imperial.mile / units.hour
TIME = 10 * units.second
MAX_SPEED = 3.1 * units.imperial.mile / units.hour

RESULT = (13.4741383682048, 3.1)


class TestMove(unittest.TestCase):
    def test_move(self):
        result = move(ACCELERATION, INITIAL_VELOCITY, TIME, MAX_SPEED)
        self.assertEqual(RESULT[0], result[0].to_value(units.meter))
        self.assertEqual(
            RESULT[1], result[1].to_value(units.imperial.mile / units.hour)
        )


if __name__ == "__main__":
    unittest.main()
