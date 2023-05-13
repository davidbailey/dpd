import unittest
from uuid import uuid4

from astropy import units
import numpy
from numpy.testing import assert_array_equal

from dpd.mechanics import KinematicBody
from dpd.mechanics.datacollection import KINEMATIC_BODY_AGENT_REPORTERS
from dpd.modeling import TransportationModel


class TestKinematicBody1DInt(unittest.TestCase):
    def test_body_1d_int(self):
        model = TransportationModel(agent_reporters=KINEMATIC_BODY_AGENT_REPORTERS)
        body = KinematicBody(
            model=model, unique_id=uuid4(), initial_position=1, initial_velocity=1
        )
        model.schedule.add(body)
        self.assertEqual(body.position, 1)
        model.step()
        self.assertEqual(body.position, 2)


class TestKinematicBody1DQuantity(unittest.TestCase):
    def test_body_1d_quantity(self):
        model = TransportationModel(
            agent_reporters=KINEMATIC_BODY_AGENT_REPORTERS, time_unit=units.second
        )
        body = KinematicBody(
            model=model,
            unique_id=uuid4(),
            initial_position=1 * units.meter,
            initial_velocity=1 * units.meter / units.second,
        )
        model.schedule.add(body)
        self.assertEqual(body.position, 1 * units.meter)
        model.step()
        self.assertEqual(body.position, 2 * units.meter)


class TestKinematicBody2DInt(unittest.TestCase):
    def test_body_2d_int(self):
        model = TransportationModel(agent_reporters=KINEMATIC_BODY_AGENT_REPORTERS)
        body = KinematicBody(
            model=model,
            unique_id=uuid4(),
            initial_position=numpy.array([1, 1]),
            initial_velocity=numpy.array([1, 1]),
        )
        model.schedule.add(body)
        assert_array_equal(body.position, numpy.array([1, 1]))
        model.step()
        assert_array_equal(body.position, numpy.array([2, 2]))


class TestKinematicBody2DQuantity(unittest.TestCase):
    def test_body_2d_quantity(self):
        model = TransportationModel(
            agent_reporters=KINEMATIC_BODY_AGENT_REPORTERS, time_unit=units.second
        )
        body = KinematicBody(
            model=model,
            unique_id=uuid4(),
            initial_position=numpy.array([1, 1]) * units.meter,
            initial_velocity=numpy.array([1, 1]) * units.meter / units.second,
        )
        model.schedule.add(body)
        assert_array_equal(body.position, numpy.array([1, 1]) * units.meter)
        model.step()
        assert_array_equal(body.position, numpy.array([2, 2]) * units.meter)


if __name__ == "__main__":
    unittest.main()
