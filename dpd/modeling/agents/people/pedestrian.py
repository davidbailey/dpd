import logging

from astropy import units
from mesa import Agent
from uuid import uuid4

from dpd.kinematics import move


class Pedestrian(Agent):
    """
    A pedestrian is a person travelling on foot, whether walking or running (Wikipedia).
    The Pedestiran is the base class for all people. E.g. a cyclist or a driver is just a pedestrian riding a bicycle or driving a motor vehicle.
    """

    def __init__(self, model, geometry, route):
        unique_id = uuid4()
        super().__init__(unique_id, model)
        self.geometry = geometry
        self.name = str(unique_id)
        self.route = route
        self.link = self.route.pop(0)
        self.segment = self.place_person_on_segment(self.link)
        self.length_on_segment = self.link.geometry.project(self.geometry) * units.meter
        self.arrived = False
        self.speed = 0 * units.imperial.mile / units.hour
        self.max_speed = 3.1 * units.imperial.mile / units.hour

    def place_person_on_segment(self, link, reversed_=True):
        if reversed_:
            segments = reversed(link.segments)
        else:
            segments = link.segments
        for segment in segments:
            if type(self) in segment.allowed_users:
                segment.occupants.append(self)
                return segment
        raise TypeError(
            "%s not in allowed_users (%s) on link %s."
            % (type(self), link.allowed_users, link.name)
        )

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
        self.segment = self.place_person_on_segment(self.link)
        self.length_on_segment = 0 * units.meter
        self.geometry = self.link.geometry.interpolate(
            self.length_on_segment.to_value(units.meter)
        )
