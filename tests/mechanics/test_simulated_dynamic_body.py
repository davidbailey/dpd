import unittest

from astropy import units

from dpd.mechanics import SimulatedDynamicBody


class TestSimulatedDynamicBody(unittest.TestCase):
    def test_simulated_dynamic_body(self):
        body = SimulatedDynamicBody(
          power=1 * units.watt,
          mass = 1 * units.kilogram
        )
        next_time, next_distance = kinematic_body.step()
        self.assertEqual(next_time, 1 * units.second)
        self.assertEqual(next_distance, 1 * units.meter)


if __name__ == "__main__":
    unittest.main()
