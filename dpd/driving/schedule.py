from pandas import timedelta_range, DataFrame
from datetime import datetime


class Schedule(DataFrame):
    """
    the schedule for a route
    """

    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

    @property
    def capacity(self, vehicle, rule="H"):
        return self.iloc[0].resample(rule).count() * vehicle.capacity

    @property
    def cost(self, vehicle, rule="H"):
        return self.iloc[0].resample(rule).count() * vehicle.operating_cost

    def to_trajectory(self):
        pass

    def from_gtfs(feed):
        pass

    def from_trip(trip, start="6 hour", end="24 hour", freq="20Min"):
        index = trip[trip.name.notnull()].name.drop_duplicates(keep="last").index
        stops = trip.loc[index].name
        schedule = DataFrame(index=stops.tolist())
        total_distance = trip.loc[index].total_distance
        trip_timedelta = (
            trip[trip.name.notnull()].name.drop_duplicates(keep="last").index.tolist()
        )
        for i in timedelta_range(start=start, end=end, freq=freq):
            schedule[i] = list(map(lambda x: (x + i).round("s"), trip_timedelta))
        return Schedule(schedule)

    def plot(self):
        pass
