import unittest
from itertools import combinations

from astropy import units
from shapely.geometry import LineString, Point

from dpd.mapping import Intersection, Link, Map
from dpd.modeling import People
from dpd.modeling.agents.people.cyclist import Cyclist
from dpd.modeling.agents.people.driver import Driver
from dpd.modeling.agents.people.pedestrian import Pedestrian


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
        segments = []
        map_.links[name] = Link(
            name,
            geometry,
            segments,
            input_intersection,
            output_intersection,
            number_of_lanes=1,
            sidewalk=True,
            cycleway="track",
            max_speed=25 * units.imperial.mile / units.hour,
        )
        map_.links[name].update_segments_from_osm(
            number_of_lanes=1, sidewalk=True, cycleway="track"
        )
    return map_


class TestPeople(unittest.TestCase):
    def test_people(self):
        self.map_ = build_test_map()
        self.map_.intersections.crs = "EPSG:4087"
        self.map_.links.crs = "EPSG:4087"
        self.people = People(self.map_)
        p1 = Driver(
            self.people.model,
            Point(0, 0),
            [
                self.people.links["[0, 1] to [1, 1]"],
                self.people.links["[0, 0] to [0, 1]"],
            ],
        )
        p2 = Cyclist(
            self.people.model,
            Point(0, 1),
            [
                self.people.links["[1, 0] to [1, 1]"],
                self.people.links["[0, 1] to [1, 0]"],
            ],
        )
        p3 = Pedestrian(
            self.people.model,
            Point(1, 0),
            [
                self.people.links["[1, 0] to [1, 1]"],
                self.people.links["[0, 1] to [1, 0]"],
            ],
        )
        for person in [p1, p2, p3]:
            self.people.add_person(person)
        self.people.simulate(10)
        self.people.plot()


if __name__ == "__main__":
    unittest.main()
