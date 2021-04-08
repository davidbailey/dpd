from itertools import combinations
import unittest

from astropy import units
from shapely.geometry import Point, LineString
from pyproj import CRS

from dpd.modeling.agents.people.driver import Driver
from dpd.mapping import Intersection, Segment, Link, Map
from dpd.modeling import ABTMMap, TransportationModel

aea = CRS.from_string("North America Albers Equal Area Conic")

def build_test_map():
    map_ = Map()
    for x in range(2):
        for y in range(2):
            map_.intersections[str([x, y])] = Intersection(str([x, y]), Point(x, y))
    for input_intersection, output_intersection in combinations(
        map_.intersections.values(), 2
    ):
        name = input_intersection.name + " to " + output_intersection.name
        geometry = LineString(
            [input_intersection.geometry, output_intersection.geometry]
        )
        map_.links[name] = Link(
            name,
            geometry,
            input_intersection,
            output_intersection,
            number_of_lanes=1,
            sidewalk=True,
            cycleway="track",
        )
    map_.intersections.crs = aea
    map_.links.crs = aea
    return map_


class TestABTMMap(unittest.TestCase):
    def test_abtmmap(self):
        self.map_ = build_test_map()
        self.model = TransportationModel()
        self.abtmmap = ABTMMap(self.model, self.map_)
        self.abtmmap.people.crs = aea
        p1 = Driver(
            self.model,
            Point(0, 0),
            [
                self.abtmmap.links["[0, 1] to [1, 1]"],
                self.abtmmap.links["[0, 0] to [0, 1]"],
            ],
        )
        p2 = Driver(
            self.model,
            Point(0, 1),
            [
                self.abtmmap.links["[1, 0] to [1, 1]"],
                self.abtmmap.links["[0, 1] to [1, 0]"],
            ],
        )
        for person in [p1, p2]:
            self.abtmmap.add_person(person)
        trajectories = self.abtmmap.simulate(10)
        self.abtmmap.plot()


if __name__ == "__main__":
    unittest.main()
