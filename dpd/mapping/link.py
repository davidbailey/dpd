"""
A link is based on an GMNS link (https://github.com/zephyr-data-specs/GMNS/blob/master/Specification/link.schema.json). However, our links are only one way: all two way links are broken into two one-way links. This means there is only one direction to consider.

Links are made up of one, two, three, or four of the following classes:
    1. Lanes. Lanes are wide enough for a motor vehicle. Bicycles and pedestrians may also use lanes. Lanes have direction from their parent link.
    2. Cycleways. Cycleways may be found between lanes and sidewalks. They are wide enough for a bicycle. Pedestrians may also use lanes. Motor vehicles may unfortunately end up in cycleways.
    3. Sidewalks. Sidewalks are on the side of a link. Bicycles and pedestrians may use sidewalks. Motor vehicles may also end up on sidewalks.
    4. Parking. A link must have at least one lane to have parking. Parking goes in between the lanes and the cycleway in the case of a protected cycleway and in between the cycleway and the sidewalk in the case of an unprotected cycleway.

Things to fix: What about a (right-hand drive) cycleway on the left side of a one-way street?
"""

import requests

from .lane import Lane
from .cycleway import Cycleway
from .sidewalk import Sidewalk
from .parking import Parking


class Link:
    """
    Note: the output_intersection of a road means that road is an input_road of that intersection. And the input_intersection of a road means that road is an output_road of that intersection
    """

    def __init__(
        self,
        name,
        geometry,
        input_intersection=None,
        output_intersection=None,
        number_of_lanes=0,
        parking=None,
        cycleway=None,
        sidewalk=None,
        **kwargs
    ):
        self.name = name
        self.geometry = geometry
        self.input_intersection = input_intersection
        if input_intersection:
            input_intersection.add_output_road(self)
        self.output_intersection = output_intersection
        if output_intersection:
            output_intersection.add_input_road(self)
        self.lanes = [None, None]
        for lane_number in range(number_of_lanes):
            lane = Lane(self, lane_number)
            self.lanes.insert(-1, lane)
        if cycleway == "lane":
            self.lanes.insert(-1, Cycleway(self))
        if parking:
            self.lanes.insert(-1, Parking(self, parking))
        if cycleway == "track":
            self.lanes.insert(-1, Cycleway(self))
        if sidewalk:
            self.lanes.insert(-1, Sidewalk(self))
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def update_lanes_from_streetmix(self, url):
        r = requests.get(url)
        street = r.json()
        lane_number = 0
        self.lanes = [None, None]
        for segment in street["data"]["street"]["segments"]:
            if segment["type"] == "drive-lane":
                lane = Lane(self, lane_number)
                self.lanes.insert(-1, lane)
                lane_number += 1
            elif segment["type"] == "parking":
                self.lanes.insert(-1, Parking(self)
            elif segment["type"] == "bike-lane":
                self.lanes.insert(-1, Cycleway(self)
            elif segment["type"] == "sidewalk":
                self.lanes.insert(-1, Sidewalk(self)
