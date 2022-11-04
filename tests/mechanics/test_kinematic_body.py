import unittest

# from astropy import units

# from dpd.mechanics import KinematicBody


class TestSimulatedKinematicBody(unittest.TestCase):
    def test_simulated_kinematic_body(self):
        """
        body = SimulatedKinematicBody()
        body.current_velocity = 1 * units.meter / units.second
        next_time, next_distance = body.step()
        self.assertEqual(next_time, 1 * units.second)
        self.assertEqual(next_distance, 1 * units.meter)
        """
        pass


if __name__ == "__main__":
    unittest.main()
