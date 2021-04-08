from itertools import combinations
import unittest

from astropy import units
from shapely.geometry import Point, LineString

from dpd.modeling.agents.people.driver import Driver
from dpd.mapping import Intersection, Segment, Link, Map
from dpd.modeling import ABTMMap, TransportationModel

def build_test_map():
    map_ = Map()
    for x in range(2):
        for y in range(2):
            map_[str([x, y])] = Intersection(str([x, y]), Point(x, y))
    for input_intersection, output_intersection in combinations(
        map_.intersections.values(), 2
    ):
        name = input_intersection.name + " to " + output_intersection.name
        geometry = LineString(
            [input_intersection.geometry, output_intersection.geometry]
        )
        map_[name] = Link(
                name,
                geometry,
                input_intersection,
                output_intersection,
                number_of_lanes=1,
                sidewalk=True,
                cycleway="track",
            )
        )
    return map_


class TestABTMMap(unittest.TestCase):
    def test_abtmmap(self):
        self.map_ = build_test_map()
        self.model = TransportationModel()
        self.abtmmap = ABTMMap(self.model, self.map_)
        p1 = Driver(
            self.model,
            Point(0, 0),
            [
                self.abtmmap.links.loc["[0, 1] to [1, 1]"]["object"],
                self.abtmmap.links.loc["[0, 0] to [0, 1]"]["object"],
            ],
        )
        p2 = Driver(
            self.model,
            Point(0, 1),
            [
                self.abtmmap.links.loc["[1, 0] to [1, 1]"]["object"],
                self.abtmmap.links.loc["[0, 1] to [1, 0]"]["object"],
            ],
        )
        for person in [p1, p2]:
            self.abtmmap.add_person(person)
        trajectories = self.abtmmap.simulate(10)
        self.abtmmap.plot()


if __name__ == "__main__":
    unittest.main()
