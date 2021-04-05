import logging

from astropy import units
from mesa import Agent
from uuid import uuid4

from dpd.kinematics import step


class Pedestrian(Agent):
    def __init__(self, model, geometry, route):
        unique_id = uuid4()
        super().__init__(unique_id, model)
        self.geometry = geometry
        self.name = str(unique_id)
        self.route = route
        self.link = self.route.pop(0)
        if self.link.sidewalk:
            self.segment = self.link.sidewalk
        elif self.link.cycleway:
            self.segment = self.link.cycleway
        else:
            self.segment = self.link.segments[-2]
        self.segment.occupants.append(self)
        self.length_on_segment = self.link.geometry.project(self.geometry) * units.meter
        self.max_speed = 3.1 * units.imperial.mile / units.hour
        self.speed = 0 * units.imperial.mile / units.hour
        self.arrived = False

    def step(self):
        if self.length_on_segment >= self.link.geometry.length * units.meter:
            logging.info(
                "%s reached end of segment, pass control to intersection" % (self.name,)
            )
            if self.route:
                # if there are still more segments, we are not at the end
                self.link.output_intersection.new_approach(self)
            else:
                # if there are no more route segments, we have arrived
                logging.info("%s arrived" % (self.name,))
                self.arrived = True
        else:
            logging.info("%s walking... no congestion for pedestrians" % (self.name,))
            self.move_forward()

    def move_forward(self):
        self.speed = min(self.max_speed, self.link.max_speed)
        self.length_on_segment += self.speed * 1 * units.second
        self.geometry = self.link.geometry.interpolate(
            self.length_on_segment.to_value(units.meter)
        )

    def proceed_through_intersection(self):
        self.segment.occupants.remove(self)
        self.link = self.route.pop(0)
        if self.link.sidewalk:
            self.segment = self.link.sidewalk
        elif self.link.cycleway:
            self.segment = self.link.cycleway
        else:
            self.segment = self.link.segments[-2]
        self.length_on_segment = 0 * units.meter
        self.segment.occupants.append(self)
        self.geometry = self.link.geometry.interpolate(
            self.length_on_segment.to_value(units.meter)
        )
