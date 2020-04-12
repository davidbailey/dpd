import unittest

from shapely.geometry import Point, LineString

from dpd.modeling import PersonAgent, TransportationModel

HOME = Point(0, 0)
WORK = Point(30, 0)

ROUTE_GEOMETRY = LineString([HOME, WORK])


class TestModel(unittest.TestCase):
    def test_model(self):
        self.model = TransportationModel()
        self.person = PersonAgent(model=self.model, home=HOME, work=WORK)
        self.person.route_geometry = ROUTE_GEOMETRY
        self.person.route_distance = 30
        self.person.route_duration = 1
        self.model.schedule.add(self.person)
        self.model.step()
        self.assertEqual(self.person.route_distance, self.person.distance)
        self.assertEqual(self.person.route_duration, self.person.travel_time)


if __name__ == "__main__":
    unittest.main()
