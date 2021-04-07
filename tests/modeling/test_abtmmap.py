from itertools import combinations
import unittest

from astropy import units
from pyproj import CRS
from shapely.geometry import Point, LineString

from dpd.modeling.agents.people.driver import Driver
from dpd.mapping import Intersection, Segment, Link, Map
from dpd.modeling import ABTMMap, TransportationModel


class TestABTMMap(unittest.TestCase):
    def test_abtmmap(self):
        self.map_ = Map()
        for x in range(2):
            for y in range(2):
                self.map_.add_intersection(Intersection(str([x, y]), Point(x, y)))
        for input_intersection, output_intersection in combinations(
            self.map_.intersections["object"], 2
        ):
            name = input_intersection.name + " to " + output_intersection.name
            geometry = LineString(
                [input_intersection.geometry, output_intersection.geometry]
            )
            self.map_.add_link(
                Link(
                    name,
                    geometry,
                    input_intersection,
                    output_intersection,
                    number_of_lanes=1,
                    max_speed=20 * units.kilometer / units.hour,
                )
            )
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

        aea = CRS.from_string("North America Albers Equal Area Conic")
        self.abtmmap.intersections.crs = aea
        self.abtmmap.links.crs = aea
        self.abtmmap.people.crs = aea
        trajectories = self.abtmmap.simulate(10)
        self.abtmmap.plot(include_links=True)


if __name__ == "__main__":
    unittest.main()
