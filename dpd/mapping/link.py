import requests

from .lane import Lane
from .cycleway import Cycleway
from .sidewalk import Sidewalk


class Way:
    """
    Note: the output_intersection of a road means that road is an input_road of that intersection. And the input_intersection of a road means that road is an output_road of that intersection
    """

    def __init__(
        self,
        name,
        geometry,
        input_intersection,
        output_intersection,
        number_of_lanes,
        cycleway=None,
        sidewalk=True,
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
        if cycleway == "track" or cycleway == "lane":
            self.cycleway = Cycleway(self, cycleway)
        else:
            self.cycleway = None
        if sidewalk:
            self.sidewalk = Sidewalk(self)
        else:
            self.sidewalk = None
        for lane_number in range(number_of_lanes):
            lane = Lane(self, lane_number)
            self.lanes.insert(-1, lane)
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def update_lanes_from_streetmix(self, url):
        r = requests.get(url)
        street = r.json()
        lane_number = 0
        self.lanes = [None, None]
        divider = False
        for segment in street["data"]["street"]["segments"]:
            if segment["type"] == "drive-lane":
                lane = Lane(self, lane_number)
                self.lanes.insert(-1, lane)
                lane_number += 1
            elif segment["type"] == "divider":
                divider = True
            elif segment["type"] == "bike-lane":
                if divider:
                    self.cycleway = Cycleway(self, "track")
                else:
                    self.cycleway = Cycleway(self, "lane")
            elif segment["type"] == "sidewalk":
                self.sidewalk = Sidewalk(self)
