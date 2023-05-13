"""
A link is based on an GMNS link (https://github.com/zephyr-data-specs/GMNS/blob/master/Specification/link.schema.json). However, our links are only one way: all two way links are broken into two one-way links. This means there is only one direction to consider.

Links are made up of one, two, three, or four of the following Segments:
    1. Lanes. Lanes are wide enough for a motor vehicle. Bicycles and pedestrians may also use segments. Lanes have direction from their parent link.
    2. Cycleways. Cycleways may be found between segments and sidewalks. They are wide enough for a bicycle. Pedestrians may also use segments. Motor vehicles may unfortunately end up in cycleways.
    3. Sidewalks. Sidewalks are on the side of a link. Bicycles and pedestrians may use sidewalks. Motor vehicles may also end up on sidewalks.
    4. Parking. A link must have at least one lane to have parking. Parking goes in between the segments and the cycleway in the case of a protected cycleway and in between the cycleway and the sidewalk in the case of an unprotected cycleway.

Things to fix: What about a (right-hand drive) cycleway on the left side of a one-way street?
"""

import requests

from .lane import Lane
from .cycleway import Cycleway
from .sidewalk import Sidewalk
from .parking import Parking


class Link:
    """
    Note: the output_intersection of a link means that link is an input_link of that intersection. And the input_intersection of a link means that link is an output_link of that intersection
    """

    def __init__(
        self,
        name,
        geometry,
        segments,
        input_intersection=None,
        output_intersection=None,
        opposite_direction_link=None,
        **kwargs
    ):
        self.name = name
        self.geometry = geometry
        self.segments = segments
        self.input_intersection = input_intersection
        if input_intersection:
            input_intersection.add_output_link(self)
        self.output_intersection = output_intersection
        if output_intersection:
            output_intersection.add_input_link(self)
        self.opposite_direction_link = opposite_direction_link
        # kwargs are useful for setting things like max_speed
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def update_segments_from_osm(
        self,
        number_of_lanes=0,
        parking=None,
        cycleway=None,
        sidewalk=None,
    ):
        self.segments = [None, None]
        segment_number = 0
        for _ in range(number_of_lanes):
            lane = Lane(self, segment_number)
            self.segments.insert(-1, lane)
            segment_number += 1
        if cycleway == "lane":
            self.segments.insert(-1, Cycleway(self, segment_number))
            segment_number += 1
        if parking:
            self.segments.insert(-1, Parking(self, segment_number, parking))
            segment_number += 1
        if cycleway == "track":
            self.segments.insert(-1, Cycleway(self, segment_number))
            segment_number += 1
        if sidewalk:
            self.segments.insert(-1, Sidewalk(self, segment_number))
            segment_number += 1

    def update_segments_from_streetmix(self, url, timeout=60):
        r = requests.get(url, timeout=timeout)
        street = r.json()
        self.segments = [None, None]
        segment_number = 0
        for segment in street["data"]["street"]["segments"]:
            if segment["type"] == "drive-lane":
                lane = Lane(self, segment_number)
                self.segments.insert(-1, lane)
                segment_number += 1
            elif segment["type"] == "parking":
                self.segments.insert(-1, Parking(self, segment_number))
                segment_number += 1
            elif segment["type"] == "bike-lane":
                self.segments.insert(-1, Cycleway(self, segment_number))
                segment_number += 1
            elif segment["type"] == "sidewalk":
                self.segments.insert(-1, Sidewalk(self, segment_number))
                segment_number += 1
