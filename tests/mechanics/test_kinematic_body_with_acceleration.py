import unittest
from uuid import uuid4

from astropy import units
import numpy
from numpy.testing import assert_array_equal

from dpd.mechanics import KinematicBodyWithAcceleration
from dpd.mechanics.datacollection import (
    KINEMATIC_BODY_WITH_ACCELERATION_AGENT_REPORTERS,
)
from dpd.modeling import TransportationModel


class TestKinematicBodyWithAcceleration1DInt(unittest.TestCase):
    def test_body_1d_int(self):
        model = TransportationModel(
            agent_reporters=KINEMATIC_BODY_WITH_ACCELERATION_AGENT_REPORTERS
        )
        body = KinematicBodyWithAcceleration(
            model=model,
            unique_id=uuid4(),
            initial_position=1,
            initial_velocity=1,
            initial_acceleration=1,
        )
        model.schedule.add(body)
        self.assertEqual(body.position, 1)
        model.step()
        self.assertEqual(body.position, 3)


class TestKinematicBodyWithAcceleration1DQuantity(unittest.TestCase):
    def test_body_1d_quantity(self):
        model = TransportationModel(
            agent_reporters=KINEMATIC_BODY_WITH_ACCELERATION_AGENT_REPORTERS,
            time_unit=units.second,
        )
        body = KinematicBodyWithAcceleration(
            model=model,
            unique_id=uuid4(),
            initial_position=1 * units.meter,
            initial_velocity=1 * units.meter / units.second,
            initial_acceleration=1 * units.meter / units.second**2,
        )
        model.schedule.add(body)
        self.assertEqual(body.position, 1 * units.meter)
        model.step()
        self.assertEqual(body.position, 3 * units.meter)


class TestKinematicBodyWithAcceleration2DInt(unittest.TestCase):
    def test_body_2d_int(self):
        model = TransportationModel(
            agent_reporters=KINEMATIC_BODY_WITH_ACCELERATION_AGENT_REPORTERS
        )
        body = KinematicBodyWithAcceleration(
            model=model,
            unique_id=uuid4(),
            initial_position=numpy.array([1, 1]),
            initial_velocity=numpy.array([1, 1]),
            initial_acceleration=numpy.array([1, 1]),
        )
        model.schedule.add(body)
        assert_array_equal(body.position, numpy.array([1, 1]))
        model.step()
        assert_array_equal(body.position, numpy.array([3, 3]))


class TestKinematicBodyWithAcceleration2DQuantity(unittest.TestCase):
    def test_body_2d_quantity(self):
        model = TransportationModel(
            agent_reporters=KINEMATIC_BODY_WITH_ACCELERATION_AGENT_REPORTERS,
            time_unit=units.second,
        )
        body = KinematicBodyWithAcceleration(
            model=model,
            unique_id=uuid4(),
            initial_position=numpy.array([1, 1]) * units.meter,
            initial_velocity=numpy.array([1, 1]) * units.meter / units.second,
            initial_acceleration=numpy.array([1, 1]) * units.meter / units.second**2,
        )
        model.schedule.add(body)
        assert_array_equal(body.position, numpy.array([1, 1]) * units.meter)
        model.step()
        assert_array_equal(body.position, numpy.array([3, 3]) * units.meter)


if __name__ == "__main__":
    unittest.main()
