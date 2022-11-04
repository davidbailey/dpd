import unittest

#from astropy import units

#from dpd.mechanics import DynamicBody


class TestSimulatedDynamicBody(unittest.TestCase):
    def test_simulated_dynamic_body(self):
        """
        body = SimulatedDynamicBody(
            power=1 * units.watt,
            mass=1 * units.kilogram,
            acceleration_limit=1 * units.meter / units.second**2,
        )
        next_time, next_distance = body.step()
        self.assertEqual(next_time, 1 * units.second)
        self.assertEqual(next_distance, 1 * units.meter)
        """
        pass


if __name__ == "__main__":
    unittest.main()
