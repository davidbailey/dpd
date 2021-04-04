import logging

from astropy import units
from mesa import Agent
from uuid import uuid4


class Cyclist(Agent):
    def __init__(self, model, geometry, route):
        unique_id = uuid4()
        super().__init__(unique_id, model)
        self.geometry = geometry
        self.name = str(unique_id)
        self.route = route
        self.link = self.route.pop(0)
        if self.link.cycleway:
            self.segment = self.link.cycleway
        else:
            self.segment = self.link.segments[-2]
        self.segment.occupants.append(self)
        self.length_on_segment = self.link.geometry.project(self.geometry) * units.meter
        self.stopping_distance = 1 * units.meter
        self.max_speed = 14 * units.imperial.mile / units.hour
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
        elif self.segment.occupants.index(self) > 0:
            logging.info(
                "%s potential for congestion %s" % (self.name, self.segment.occupants)
            )
            my_index = self.segment.occupants.index(self)
            person_in_front_of_me = self.segment.occupants[my_index - 1]
            if (
                person_in_front_of_me.length_on_segment
                < self.length_on_segment + self.stopping_distance
            ):  # congestion! let's see if we can change segments
                if self.link.segments[self.segment.segment_number + 1]:
                    if self.attempt_segment_change(
                        self.link.segments[self.segment.segment_number + 1]
                    ):  # returns false if segment change successful, true if unsuccessful
                        if self.link.segments[self.segment.segment_number - 1]:
                            if not self.attempt_segment_change(
                                self.link.segments[self.segment.segment_number - 1]
                            ):
                                self.move_forward()
                    else:  # refactor this to a go() function
                        self.move_forward()
                else:
                    self.stop()  # stuck in traffic :( you are traffic
            else:
                # freeflow traffic, person too far ahead
                self.move_forward()
        else:
            logging.info("%s freeflow traffic, no one ahead" % (self.name,))
            self.move_forward()

    def move_forward(self):
        self.speed = min(self.max_speed, self.link.max_speed)
        self.length_on_segment += self.speed * 1 * units.second
        self.geometry = self.link.geometry.interpolate(
            self.length_on_segment.to_value(units.meter)
        )

    def stop(self):
        self.speed = 0 * units.meter / units.second

    def attempt_segment_change(self, segment):
        logging.info("%s attempting segment change" % (self.name,))
        index_of_new_person_in_front_of_me = bisect.bisect_left(
            list(map(lambda x: x.length_on_segment.to_value(units.meter), segment.occupants)),
            self.length_on_segment.to_value(units.meter),
        )
        index_of_new_person_behind_me = bisect.bisect_right(
            list(map(lambda x: x.length_on_segment.to_value(units.meter), segment.occupants)),
            self.length_on_segment.to_value(units.meter),
        )
        if index_of_new_person_in_front_of_me > 0:
            new_person_in_front_of_me = segment[index_of_new_person_in_front_of_me]
            if (
                not new_person_in_front_of_me
                > self.length_on_segment + self.stopping_distance
            ):
                return True
        if index_of_new_person_behind_me < len(segment.occupants):
            new_person_behind_me = segment[index_of_new_person_behind_me]
            if (
                not new_person_behind_me.length_on_segment
                + new_person_behind_me.stopping_distance
                < self.length_on_segment
            ):
                return True
        self.segment.occupants.remove(self)
        self.segment = segment
        if index_of_new_person_behind_me < len(segment.occupants):
            self.segment.occupants.insert(index_of_person_behind_me, self)
        return False

    def proceed_through_intersection(self):
        self.segment.occupants.remove(self)
        self.link = self.route.pop(0)
        if self.link.cycleway:
            self.segment = self.link.cycleway
        else:
            self.segment = self.link.segments[-2]
        self.length_on_segment = 0 * units.meter
        self.segment.occupants.append(self)
        self.geometry = self.link.geometry.interpolate(
            self.length_on_segment.to_value(units.meter)
        )
