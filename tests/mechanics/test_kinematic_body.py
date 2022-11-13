import unittest
from uuid import uuid4

from astropy import units
import numpy
from numpy.testing import assert_array_equal

from dpd.mechanics import KinematicBody
from dpd.mechanics.datacollection import KinematicBodyDataCollector
from dpd.modeling import TransportationModel


class TestKinematic1DInt(unittest.TestCase):
    def test_body_1d_int(self):
        model = TransportationModel(datacollector=KinematicBodyDataCollector)
        body = KinematicBody(
            model=model, unique_id=uuid4(), initial_position=1, initial_velocity=1
        )
        model.step()
        self.assertEqual(body.position, 1)


class TestKinematicBody1DQuantity(unittest.TestCase):
    def test_body_1d_quantity(self):
        model = TransportationModel(datacollector=KinematicBodyDataCollector)
        body = KinematicBody(
            model=model,
            unique_id=uuid4(),
            initial_position=1 * units.meter,
            initial_velocity=1 * units.meter / units.second,
        )
        model.step()
        self.assertEqual(body.position, 1 * units.meter)


class TestKinematicBody2DInt(unittest.TestCase):
    def test_body_2d_int(self):
        model = TransportationModel(datacollector=KinematicBodyDataCollector)
        body = KinematicBody(
            model=model,
            unique_id=uuid4(),
            initial_position=numpy.array([1, 1]),
            initial_velocity=numpy.array([1, 1]),
        )
        model.step()
        assert_array_equal(body.position, numpy.array([1, 1]))


class TestKinematicBody2DQuantity(unittest.TestCase):
    def test_body_2d_quantity(self):
        model = TransportationModel(datacollector=KinematicBodyDataCollector)
        body = KinematicBody(
            model=model,
            unique_id=uuid4(),
            initial_position=numpy.array([1, 1]) * units.meter,
            initial_velocity=numpy.array([1, 1]) * units.meter / units.second,
        )
        model.step()
        assert_array_equal(body.position, numpy.array([1, 1]) * units.meter)


if __name__ == "__main__":
    unittest.main()
