import logging
from uuid import uuid4

from mesa import Agent


class PersonAgent(Agent):
    """
    A person
    """

    def __init__(self, model, home, work, unique_id=None):
        if not unique_id:
            unique_id = uuid4()
        super().__init__(unique_id, model)
        self.home = home
        self.pos = home  # set initial position at home
        self.work = work
        self.speed = 30  # meters / step
        self.travel_time = 0
        self.distance = 0
        self.vehicle = None

    def step(self):
        if self.pos != self.work:
            self.travel_time += 1
            if self.vehicle:
                self.drive()
            else:
                self.walk()
            if self.distance >= self.route_geometry.length:
                self.pos = self.work
                self.distance = self.route_geometry.length
                logging.info(
                    "Person %s arrived: traveled %s meters (predicted %s) in %s steps (predicted %s)."
                    % (
                        self.unique_id,
                        self.distance,
                        self.route_distance,
                        self.travel_time,
                        self.route_duration,
                    )
                )

    def walk(self):
        self.distance += self.speed

    def drive(self):
        self.distance += self.vehicle.max_speed
