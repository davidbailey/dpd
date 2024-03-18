from logging import warn

from astropy.units import Quantity, meter
from mesa import Agent
from numpy import inf, minimum

from dpd.mechanics import KinematicBodyWithAcceleration


class EdgesDriver(Agent):
    def __init__(
        self,
        body,
        edges,
        initial_driver_position_offset=None,
        driver_max_velocity=None,
        driver_final_velocity=None,
        *args,
        **kwargs
    ):
        """
        body: (Body): a body to drive along edges
        edges (list of dict): a list of dictionaries of distances (int or float) and (optionally) speed limits (int or float) for segments along a route.
        """
        super().__init__(*args, **kwargs)
        if driver_max_velocity is None and not isinstance(body, KinematicBodyWithAcceleration):
            warn(
                "driver_max_velocity is not set: Driver will not accelerate after slowing due to maxspeed. Try setting driver_max_velocity equal to initial_velocity"
            )
        self.body = body
        self.edges = edges
        self.distance_unit = 0 * edges[0]["distance"]
        if initial_driver_position_offset is None:
            self.driver_position_offset = 0 * self.distance_unit
        else:
            self.driver_position_offset = initial_driver_position_offset
        self.driver_max_velocity = driver_max_velocity
        self.driver_final_velocity = driver_final_velocity
        self.begin_next_edge(extra_position=0 * self.distance_unit)

    @property
    def geometry(self):
        if isinstance(self.body.position, Quantity):
            return self.current_edge.geometry.interpolate(self.body.position.to(meter).value)
        return self.current_edge.geometry.interpolate(self.body.position)

    @property
    def position(self):
        return self.driver_position_offset + self.body.position

    def begin_next_edge(self, extra_position):
        self.current_edge = self.edges.pop(0)
        self.driver_position_offset += self.body.position
        if extra_position is not None:
            self.body.position = extra_position
        else:
            self.body.position = 0 * self.distance_unit
        self.body.max_position = self.current_edge["distance"]
        if isinstance(self.body, KinematicBodyWithAcceleration):
            self.body.acceleration = self.body.initial_acceleration
        if self.driver_max_velocity is not None:
            self.body.max_velocity = minimum(
                self.current_edge.get("maxspeed", inf), self.driver_max_velocity
            )
        else:
            self.body.max_velocity = self.current_edge.get("maxspeed", inf)
        if len(self.edges) > 0:
            self.body.final_velocity = self.edges[0].get("maxspeed")
        else:
            self.body.final_velocity = self.driver_final_velocity

    def end_current_edge(self, extra_position):
        if len(self.edges) == 0:
            self.model.schedule.remove(self)
        else:
            self.begin_next_edge(extra_position=extra_position)

    def step(self):
        extra_position = 0 * self.distance_unit
        self.body.step()
        if self.body.position == self.body.max_position:
            self.end_current_edge(extra_position=extra_position)
