from functools import lru_cache
import matplotlib.pyplot as plt
from shapely.geometry import Point

from .stop import Stop
from dpd.geometry import MovingDict
from dpd.utils import epsg4326_to_aea, timestring_to_timeobject

class Trip(MovingDict):
    """
    A class to describe a person or vehicle going from place to place.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_stop(self, geometry, distance=0, name="", arrival_time=None, departure_time=None, **kwargs):
        if  arrival_time:
            self.data[arrival_time] = Stop(name=name, geometry=geometry, distance = distance, **kwargs)
        if departure_time:
            self.data[departure_time] = Stop(name=name, geometry=geometry, distance = distance, **kwargs)
 
    def _stop_id_to_distance(feed, aea_line, stop_id):
        stop = feed.stops[feed.stops.stop_id == stop_id]
        stop_point = shapely.geometry.point.Point(stop.stop_lon, stop.stop_lat)
        stop_point_aea = epsg4326_to_aea(stop_point)
        distance = aea_line.project(stop_point_aea)
        return distance

    def from_gtfs(feed, route_id, service_id, shape_id=None):
        """
        A way to build a trip from GTFS data.
        Args:
            feed: the GTFS feed that contains the route
            route_id (int): the route_id for the route
            service_id (int): the service_id for the trip
            shape_id (int): the shape_id for the route
        Returns:
            dpd.driving.Trip: a Trip
        """
        trips = feed.trips[
            (feed.trips["route_id"] == route_id) & (feed.trips["service_id"] == service_id)
        ]["trip_id"]
        if not shape_id:
            shape_id = feed.trips[feed.trips["trip_id"] == trips.iloc[0]].shape_id.iloc[0]
        line = feed.build_geometry_by_shape([shape_id])[shape_id]
        aea_line = epsg4326_to_aea(line)
        
        @lru_cache(maxsize=128)  # adds a little complexity, but reduces runtime by half :)
        def stop_id_to_distance_cached(stop_id):
            return _stop_id_to_distance(feed, aea_line, stop_id)
        trip = self.__init__()
        for trip_id in trips:
            d = feed.stop_times[feed.stop_times["trip_id"] == trip_id].copy()
            d["arrival_time_object"] = d.arrival_time.map(timestring_to_timeobject)
            d["departure_time_object"] = d.departure_time.map(timestring_to_timeobject)
            d["distance"] = d.stop_id.map(stop_id_to_distance_cached)
            plt.plot(d.arrival_time_object, d.distance / 1000)
        for index, stop in d.iterrows():
            trip.add_stop(
                name="",
                geometry=Point(0,0),
                distance=stop["distance"],
                arrival_time=stop["arrival_time_object"],
                departure_time=stop["departure_time_object"]
            )
        return trip

    def plot_schedule(self, **kwargs):
        geodataframe = self.to_geodataframe(columns=["name", "geometry", "distance"])
        geodataframe["distance"].plot(**kwargs)
        annotated_stops = []
        for idx, row in geodataframe.iterrows():
            if row["name"] not in annotated_stops:
                plt.annotate(
                    text=row["name"],
                    xy=(idx, row["distance"])
                )
            annotated_stops.append(row["name"])
