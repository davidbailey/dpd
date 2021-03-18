from astropy import units
from mesa import Agent
from uuid import uuid4


class Driver(Agent):
    def __init__(self, model, geometry, route):
        unique_id = uuid4()
        super().__init__(unique_id, model)
        self.geometry = geometry
        self.name = str(unique_id)
        self.route = route
        self.road = self.route.pop()
        self.lane = self.road.lanes[-2]
        self.lane.occupants.append(self)
        self.length_on_lane = self.road.geometry.project(self.geometry) * units.meter
        self.stopping_distance = 1 * units.meter
        self.max_speed = 100 * units.imperial.mile / units.hour
        self.speed = 0 * units.imperial.mile / units.hour

    def step(self):
        print(self.name, self.geometry)
        if self.length_on_lane >= self.road.geometry.length:
            print(self.name, "reached end of lane, pass control to intersection")
            if self.route:
                # if there are still more segments, we are not at the end
                self.road.output_intersection.new_approach(self)
            else:
                # if there are no more route segments, we have arrived
                print(self.name, "Arrived")
        elif self.lane.occupants.index(self) > 0:
            print(self.name, "potential for congestion", self.lane.occupants)
            my_index = self.lane.occupants.index(self)
            person_in_front_of_me = self.lane.occupants[my_index - 1]
            if (
                person_in_front_of_me.length_on_lane
                < self.length_on_lane + self.stopping_distance
            ):  # congestion! let's see if we can change lanes
                if self.road.lanes[self.lane.lane_number + 1]:
                    if self.attempt_lane_change(
                        self.road.lanes[self.lane.lane_number + 1]
                    ):  # returns false if lane change successful, true if unsuccessful
                        if self.road.lanes[self.lane.lane_number - 1]:
                            if not self.attempt_lane_change(
                                self.road.lanes[self.lane.lane_number - 1]
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
            # print(self.name, "freeflow traffic, no one ahead")
            self.move_forward()

    def move_forward(self):
        # print(self.name, self.length_on_lane)
        self.speed = min(self.max_speed, self.road.max_speed)
        self.length_on_lane += self.speed * 1 * units.second
        self.geometry = self.road.geometry.interpolate(
            self.length_on_lane.to_value(units.meter)
        )

    def stop(self):
        self.speed = 0 * units.meter / units.second

    def attempt_lane_change(self, lane):
        # print(self.name, "attempting lane change")
        index_of_new_person_in_front_of_me = bisect.bisect_left(
            list(map(lambda x: x.length_on_lane.to_value(units.meter), lane.occupants)),
            self.length_on_lane.to_value(units.meter),
        )
        index_of_new_person_behind_me = bisect.bisect_right(
            list(map(lambda x: x.length_on_lane.to_value(units.meter), lane.occupants)),
            self.length_on_lane.to_value(units.meter),
        )
        if index_of_new_person_in_front_of_me > 0:
            new_person_in_front_of_me = lane[index_of_new_person_in_front_of_me]
            if (
                not new_person_in_front_of_me
                > self.length_on_lane + self.stopping_distance
            ):
                return True
        if index_of_new_person_behind_me < len(lane.occupants):
            new_person_behind_me = lane[index_of_new_person_behind_me]
            if (
                not new_person_behind_me.length_on_lane
                + new_person_behind_me.stopping_distance
                < self.length_on_lane
            ):
                return True
        self.lane.occupants.remove(self)
        self.lane = lane
        if index_of_new_person_behind_me < len(lane.occupants):
            self.lane.occupants.insert(index_of_person_behind_me, self)
        return False

    def proceed_through_intersection(self):
        if self in self.lane.occupants:
            self.lane.occupants.remove(self)
        else:
            print("ERROR", self, self.lane, self.lane.occupants)
        self.road = self.route.pop()
        self.lane = self.road.lanes[-2]
        self.length_on_lane = 0 * units.meter
        self.lane.occupants.append(self)
        self.geometry = self.road.geometry.interpolate(
            self.length_on_lane.to_value(units.meter)
        )
