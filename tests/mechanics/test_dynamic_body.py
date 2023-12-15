import unittest
from uuid import uuid4

import numpy
from astropy import units
from numpy.testing import assert_array_equal

from dpd.mechanics import DynamicBody
from dpd.mechanics.datacollection import DYNAMIC_BODY_AGENT_REPORTERS
from dpd.modeling import TransportationModel


class TestDynamicBody1DInt(unittest.TestCase):
    def test_body_1d_int(self):
        model = TransportationModel(agent_reporters=DYNAMIC_BODY_AGENT_REPORTERS)
        body = DynamicBody(
            model=model,
            unique_id=uuid4(),
            initial_position=1,
            initial_velocity=1,
            initial_acceleration=1,
            power=1,
            mass=1,
        )
        model.schedule.add(body)
        self.assertEqual(body.position, 1)
        model.step()
        self.assertEqual(body.position, 3)
        model.step()
        self.assertEqual(body.position, 5.5)


class TestDynamicBody1DQuantity(unittest.TestCase):
    def test_body_1d_quantity(self):
        model = TransportationModel(
            agent_reporters=DYNAMIC_BODY_AGENT_REPORTERS,
            time_unit=units.second,
        )
        body = DynamicBody(
            model=model,
            unique_id=uuid4(),
            initial_position=1 * units.meter,
            initial_velocity=1 * units.meter / units.second,
            initial_acceleration=1 * units.meter / units.second**2,
            power=1 * units.watt,
            mass=1 * units.kilogram,
        )
        model.schedule.add(body)
        self.assertEqual(body.position, 1 * units.meter)
        model.step()
        self.assertEqual(body.position, 3 * units.meter)
        model.step()
        self.assertEqual(body.position, 5.5 * units.meter)


class TestDynamicBody2DInt(unittest.TestCase):
    def test_body_2d_int(self):
        model = TransportationModel(agent_reporters=DYNAMIC_BODY_AGENT_REPORTERS)
        body = DynamicBody(
            model=model,
            unique_id=uuid4(),
            initial_position=numpy.array([1, 1]),
            initial_velocity=numpy.array([1, 1]),
            initial_acceleration=numpy.array([1, 1]),
            power=numpy.array([1]),
            mass=numpy.array([1]),
        )
        model.schedule.add(body)
        assert_array_equal(body.position, numpy.array([1, 1]))
        model.step()
        assert_array_equal(body.position, numpy.array([3, 3]))
        model.step()
        assert_array_equal(body.position, numpy.array([5.5, 5.5]))


class TestDynamicBody2DQuantity(unittest.TestCase):
    def test_body_2d_quantity(self):
        model = TransportationModel(
            agent_reporters=DYNAMIC_BODY_AGENT_REPORTERS,
            time_unit=units.second,
        )
        body = DynamicBody(
            model=model,
            unique_id=uuid4(),
            initial_position=numpy.array([1, 1]) * units.meter,
            initial_velocity=numpy.array([1, 1]) * units.meter / units.second,
            initial_acceleration=numpy.array([1, 1]) * units.meter / units.second**2,
            power=numpy.array([1]) * units.watt,
            mass=numpy.array([1]) * units.kilogram,
        )
        model.schedule.add(body)
        assert_array_equal(body.position, numpy.array([1, 1]) * units.meter)
        model.step()
        assert_array_equal(body.position, numpy.array([3, 3]) * units.meter)
        model.step()
        assert_array_equal(body.position, numpy.array([5.5, 5.5]) * units.meter)


if __name__ == "__main__":
    unittest.main()
