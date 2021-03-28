import logging

from astropy import units
from mesa import Agent
from uuid import uuid4


class Pedestrian(Agent):
    def __init__(self, model, geometry, route):
        unique_id = uuid4()
        super().__init__(unique_id, model)
        self.geometry = geometry
        self.name = str(unique_id)
        self.route = route
        self.road = self.route.pop(0)
        if self.road.sidewalk:
            self.lane = self.road.sidewalk
        elif self.road.cycleway:
            self.lane = self.road.cycleway
        else:
            self.lane = self.road.lanes[-2]
        self.lane.occupants.append(self)
        self.length_on_lane = self.road.geometry.project(self.geometry) * units.meter
        self.max_speed = 3.1 * units.imperial.mile / units.hour
        self.speed = 0 * units.imperial.mile / units.hour
        self.arrived = False

    def step(self):
        if self.length_on_lane >= self.road.geometry.length * units.meter:
            logging.info(
                "%s reached end of lane, pass control to intersection" % (self.name,)
            )
            if self.route:
                # if there are still more segments, we are not at the end
                self.road.output_intersection.new_approach(self)
            else:
                # if there are no more route segments, we have arrived
                logging.info("%s arrived" % (self.name,))
                self.arrived = True
        else:
            logging.info("%s walking... no congestion for pedestrians" % (self.name,))
            self.move_forward()

    def move_forward(self):
        self.speed = min(self.max_speed, self.road.max_speed)
        self.length_on_lane += self.speed * 1 * units.second
        self.geometry = self.road.geometry.interpolate(
            self.length_on_lane.to_value(units.meter)
        )

    def proceed_through_intersection(self):
        self.lane.occupants.remove(self)
        self.road = self.route.pop(0)
        if self.road.sidewalk:
            self.lane = self.road.sidewalk
        elif self.road.cycleway:
            self.lane = self.road.cycleway
        else:
            self.lane = self.road.lanes[-2]
        self.length_on_lane = 0 * units.meter
        self.lane.occupants.append(self)
        self.geometry = self.road.geometry.interpolate(
            self.length_on_lane.to_value(units.meter)
        )
