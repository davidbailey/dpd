from functools import lru_cache

import matplotlib.pyplot as plt
import shapely

from dpd.utils import epsg4326_to_aea

def _stop_id_to_distance(feed, aea_line, stop_id):
    stop = feed.stops[feed.stops.stop_id == stop_id]
    stop_point = shapely.geometry.point.Point(stop.stop_lon, stop.stop_lat)
    stop_point_aea = epsg4326_to_aea(stop_point)
    distance = aea_line.project(stop_point_aea)
    return distance


def plot_schedule(feed, route_id, service_id, shape_id=None):
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

    for trip_id in trips:
        d = feed.stop_times[feed.stop_times["trip_id"] == trip_id].copy()
        d["arrival_time_object"] = d.arrival_time.map(timestring_to_timeobject)
        d["departure_time_object"] = d.departure_time.map(timestring_to_timeobject)
        d["distance"] = d.stop_id.map(stop_id_to_distance_cached)
        plt.plot(d.arrival_time_object, d.distance / 1000)
    plt.xlabel("Time of Day")
    plt.ylabel("Distance on Route")
    plt.show()
