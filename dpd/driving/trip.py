from datetime import timedelta

from astropy import units
from astropy.time import TimeDelta
from astropy.visualization import quantity_support
from geopandas import GeoDataFrame
from movingpandas import Trajectory
from pandas import concat, MultiIndex
from shapely.geometry import Point

from dpd.utils import timestring_to_timeobject


class Trip(GeoDataFrame):
    """
    a time-indexed drive along a route
    """

    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

    @property
    def stops(self):
        index = MultiIndex.from_product(
            [self.name.dropna().drop_duplicates(), ["Arrival", "Departure"]],
            names=["Stop", "Arriva/Departure"],
        )
        return concat([
            self.dropna().drop_duplicates(subset=["name"], keep="first"),
            self.dropna().drop_duplicates(subset=["name"], keep="last")
        ]).sort_index().reset_index().set_index(index)

    def in_vehicle_travel_time(self, origin_stop, destination_stop):
        return (
            self.stops.loc[origin_stop, "Departure"].total_time
            - self.stops.loc[destination_stop, "Arrival"].total_time
        )

    def reverse_distance(self):
        """
        Useful for plotting two trips that go in different directions on the same plot.
        """
        total_distance = self.total_distance.iloc[-1]
        self["total_distance"] = self["total_distance"].map(
            lambda x: total_distance - x
        )
        return self

    def plot_schedule(self, ax, include_stops=True):
        with quantity_support():
            # self.total_distance.plot(ax=ax)
            ax.plot(
                self.index, self.total_distance.map(lambda x: x.to(units.meter).value)
            )
            if include_stops:
                for index, row in self.stops.iterrows():
                    ax.axhline(
                        row["total_distance"].to(units.meter).value, linestyle="dashed"
                    )
                    ax.text(
                        ax.get_xlim()[1],
                        row["total_distance"].to(units.meter).value,
                        row["name"],
                    )

    def to_trajectory(self, index):
        return Trajectory(self, index)

    @staticmethod
    def from_gtfs(feed, trip_id):
        if feed.dist_units == "mi":
            units.imperial.enable()
        trip = feed.stop_times[feed.stop_times["trip_id"] == trip_id]
        new_trip = []
        t = timestring_to_timeobject(trip.iloc[0].arrival_time)
        start_time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        for index, row in trip.iterrows():
            stop = feed.stops[feed.stops["stop_id"] == row.stop_id].iloc[0]
            t = timestring_to_timeobject(row.arrival_time)
            arrival_time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
            t = timestring_to_timeobject(row.departure_time)
            departure_time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
            for time in [arrival_time, departure_time]:
                new_trip.append(
                    {
                        "geometry": Point(stop.stop_lon, stop.stop_lat),
                        "name": stop.stop_name,
                        "timedelta": time,
                        "total_distance": row.shape_dist_traveled
                        * units.Unit(feed.dist_units),
                        "total_time": (time - start_time).seconds * units.second,
                    }
                )
        return Trip(GeoDataFrame(new_trip).set_index("timedelta"))

    @staticmethod
    def from_model(df, route, include_geometry=True):
        df["total_distance"] = df["position"]
        df["total_time"] = df["time"]
        df["timedelta"] = df.time.map(lambda x: TimeDelta(x).to_datetime())
        df.set_index("timedelta", inplace=True)
        columns = ["name", "total_time", "total_distance"]
        if include_geometry:
            route.to_crs("North America Albers Equal Area Conic", inplace=True)
            df["geometry"] = df.apply(
                lambda row: route.way.interpolate(row.position.value), axis=1
            )
            columns.append("geometry")
        return Trip(GeoDataFrame(df, crs=route.crs)[columns])
