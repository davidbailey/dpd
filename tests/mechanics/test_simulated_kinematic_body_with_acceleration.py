import unittest

from astropy import units

from dpd.mechanics import SimulatedKinematicBodyWithAcceleration


class TestSimulatedKinematicBodyWithAcceleration(unittest.TestCase):
    def test_simulated_kinematic_body_with_acceleration(self):
        body = TestSimulatedKinematicBodyWithAcceleration(
            initial_acceleration=1 * units.meter / units.second**2,
            velocity_limit=1 * units.meter / units.second,
        )
        next_time, next_distance = body.step()
        self.assertEqual(next_time, 1 * units.second)
        self.assertEqual(next_distance, 1 * units.meter)


if __name__ == "__main__":
    unittest.main()
