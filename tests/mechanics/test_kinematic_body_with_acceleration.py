import unittest

#from astropy import units

#from dpd.mechanics import KinematicBodyWithAcceleration


class TestSimulatedKinematicBodyWithAcceleration(unittest.TestCase):
    def test_simulated_kinematic_body_with_acceleration(self):
        """
        body = SimulatedKinematicBodyWithAcceleration(
            velocity_limit=1 * units.meter / units.second,
        )
        body.current_acceleration = 1 * units.meter / units.second**2
        next_time, next_distance = body.step()
        self.assertEqual(next_time, 1 * units.second)
        self.assertEqual(next_distance, 1 * units.meter)
        """
        pass


if __name__ == "__main__":
    unittest.main()
