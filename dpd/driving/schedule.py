from movingpandas import TrajectoryCollection
from pandas import timedelta_range, DataFrame

from .trip import Trip


class Schedule:
    """
    the schedule for a route
    """

    def __init__(self, trips=None, *args, **kwargs):
        if trips:
            self.trips = trips
        else:
            self.trips = {}

    def add_trip(self, index, trip):
        self.trips[index] = trip

    @property
    def capacity(self, vehicle, rule="H"):
        return self.schedule.iloc[0].resample(rule).count() * vehicle.capacity

    @property
    def cost(self, vehicle, rule="H"):
        return self.schedule.iloc[0].resample(rule).count() * vehicle.operating_cost

    @property
    def schedule(self):
        schedule = []
        for trip in self.trips:
            trip_to_add = self.trips[trip].stops.timedelta
            trip_to_add.name = trip
            schedule.append(trip_to_add)
        return DataFrame(schedule).transpose()

    def reverse_distance(self):
        for trip in self.trips:
            self.trips[trip].reverse_distance()

    def plot_schedule(self, ax):
        for trip in self.trips:
            self.trips[trip].plot_schedule(ax=ax, include_stops=False)

    def to_trajectory_collection(self):
        trajectory_collection = []
        for trip in self.trips:
            trajectory_collection.append(self.trips[trip].to_trajectory(trip))
        return TrajectoryCollection(trajectory_collection)

    @staticmethod
    def from_gtfs(feed, route_id, direction_id):
        schedule = Schedule()
        trips = feed.trips[
            (feed.trips.route_id == route_id)
            & (feed.trips.direction_id == direction_id)
        ]
        for index, trip in trips.iterrows():
            schedule.add_trip(trip.trip_id, Trip.from_gtfs(feed, trip.trip_id))
        return schedule

    @staticmethod
    def from_trip(trip, start="6 hour", end="24 hour", freq="20Min"):
        index = 0
        schedule = Schedule()
        for td in timedelta_range(start=start, end=end, freq=freq):
            trip_to_add = trip.copy()
            trip_to_add.index = trip_to_add.index + td
            schedule.add_trip(index, Trip(trip_to_add))
            index += 1
        return schedule
