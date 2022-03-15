from astropy import units
from astropy.visualization import quantity_support
from geopandas import GeoDataFrame
from movingpandas import Trajectory
from pandas import MultiIndex


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
        return self.dropna().reset_index().set_index(index)

    def in_vehicle_travel_time(self, origin_stop, destination_stop):
        return (
            self.stops.loc[origin_stop, "Departure"].total_time
            - self.stops.loc[destination_stop, "Arrival"].total_time
        )

    def reverse_distance(self):
        """
        Useful for plotting two trips that go in different directions on the same plot.
        """
        total_distance = self.total_distance.tolist()
        total_distance.reverse()
        self["total_distance"] = total_distance
        return self

    def plot_schedule(self, ax, include_stops=True):
        with quantity_support():
            # self.total_distance.plot(ax=ax)
            ax.plot(
                self.index, self.total_distance.map(lambda x: x.to(units.meter).value)
            )
            if include_stops:
                for index, row in self.stops.iterrows():
                    ax.axhline(row["total_distance"], linestyle="dashed")
                    ax.text(ax.get_xlim()[1], row["total_distance"], row["name"])

    def to_trajectory(self, index):
        return Trajectory(self, index)

    @staticmethod
    def from_gtfs(feed):
        pass
