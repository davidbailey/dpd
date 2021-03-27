from itertools import combinations
import unittest

from astropy import units
from pyproj import CRS
from shapely.geometry import Point, LineString

from dpd.mapping import Intersection, Lane, Road, Map
from dpd.modeling import ABTMMap, Driver, TransportationModel


class TestABTMMap(unittest.TestCase):
    def test_abtmmap(self):
        self.map_ = Map()
        for x in range(2):
            for y in range(2):
                self.map_.add_intersection(Intersection(str([x, y]), Point(x, y)))
        for input_intersection, output_intersection in combinations(
            self.map_.intersections["Intersection"], 2
        ):
            name = input_intersection.name + " to " + output_intersection.name
            geometry = LineString(
                [input_intersection.geometry, output_intersection.geometry]
            )
            self.map_.add_road(
                Road(
                    name,
                    geometry,
                    input_intersection,
                    output_intersection,
                    1,
                    max_speed=20 * units.kilometer / units.hour,
                )
            )
        self.model = TransportationModel()
        self.abtmmap = ABTMMap(self.model, self.map_)
        p1 = Driver(
            self.model,
            Point(0, 0),
            [
                self.abtmmap.roads.loc["[0, 1] to [1, 1]"]["Road"],
                self.abtmmap.roads.loc["[0, 0] to [0, 1]"]["Road"],
            ],
        )
        p2 = Driver(
            self.model,
            Point(0, 1),
            [
                self.abtmmap.roads.loc["[1, 0] to [1, 1]"]["Road"],
                self.abtmmap.roads.loc["[0, 1] to [1, 0]"]["Road"],
            ],
        )
        for person in [p1, p2]:
            self.abtmmap.add_person(person)

        aea = CRS.from_string("North America Albers Equal Area Conic")
        self.abtmmap.intersections.crs = aea
        self.abtmmap.roads.crs = aea
        self.abtmmap.people.crs = aea
        trajectories = self.abtmmap.simulate(10)
        self.abtmmap.plot(include_roads=True)


if __name__ == "__main__":
    unittest.main()
