import logging

from astropy import units
import bisect

from dpd.kinematics import move
from .pedestrian import Pedestrian


class Driver(Pedestrian):
    """
    A person driving a motor vehicle
    """

    def __init__(self, model, geometry, route):
        super().__init__(model, geometry, route)
        self.stopping_distance = 1 * units.meter
        self.max_speed = 100 * units.imperial.mile / units.hour
        self.acceleration = 2.5 * units.meter / (units.second * units.second)
        self.deceleration = -self.acceleration

    def step(self):
        if self.length_on_segment >= self.link.length * units.meter:
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

    def stop(self):
        distance, self.speed = move(
            self.deceleration,
            self.speed,
            1 * units.second,
            0 * units.meter / units.second,
        )
        self.length_on_segment += distance

    def attempt_segment_change(self, segment):
        logging.info("%s attempting segment change" % (self.name,))
        index_of_new_person_in_front_of_me = bisect.bisect_left(
            list(
                map(
                    lambda x: x.length_on_segment.to_value(units.meter),
                    segment.occupants,
                )
            ),
            self.length_on_segment.to_value(units.meter),
        )
        index_of_new_person_behind_me = bisect.bisect_right(
            list(
                map(
                    lambda x: x.length_on_segment.to_value(units.meter),
                    segment.occupants,
                )
            ),
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
            self.segment.occupants.insert(index_of_new_person_behind_me, self)
        return False
