import unittest
from uuid import uuid4

from astropy import units
import numpy
from numpy.testing import assert_array_equal

from dpd.mechanics import Body
from dpd.mechanics.datacollection import BODY_AGENT_REPORTERS
from dpd.modeling import TransportationModel


class TestBody1DInt(unittest.TestCase):
    def test_body_1d_int(self):
        model = TransportationModel(agent_reporters=BODY_AGENT_REPORTERS)
        body = Body(model=model, unique_id=uuid4(), initial_position=1)
        self.assertEqual(body.position, 1)


class TestBody1DQuantity(unittest.TestCase):
    def test_body_1d_quantity(self):
        model = TransportationModel(agent_reporters=BODY_AGENT_REPORTERS)
        body = Body(model=model, unique_id=uuid4(), initial_position=1 * units.meter)
        self.assertEqual(body.position, 1 * units.meter)


class TestBody2DInt(unittest.TestCase):
    def test_body_2d_int(self):
        model = TransportationModel(agent_reporters=BODY_AGENT_REPORTERS)
        body = Body(
            model=model, unique_id=uuid4(), initial_position=numpy.array([1, 1])
        )
        assert_array_equal(body.position, numpy.array([1, 1]))


class TestBody2DQuantity(unittest.TestCase):
    def test_body_2d_quantity(self):
        model = TransportationModel(agent_reporters=BODY_AGENT_REPORTERS)
        body = Body(
            model=model,
            unique_id=uuid4(),
            initial_position=numpy.array([1, 1]) * units.meter,
        )
        assert_array_equal(body.position, numpy.array([1, 1]) * units.meter)


if __name__ == "__main__":
    unittest.main()
