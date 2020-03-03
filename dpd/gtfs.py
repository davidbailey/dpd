import pyproj
import shapely
from shapely.ops import transform
from dpd.utils import epsg4326_to_aea
import matplotlib.pyplot as plt

import requests
import gtfstk
import tempfile
import folium
import mplleaflet
import geopandas
import numpy
from matplotlib import pyplot
from shapely.geometry import Point
from functools import partial, lru_cache

from dpd.utils import timestring_to_timeobject

def url2gtfs(url, dist_units="mi"):
    """
    Downloads a gtfs zip into a temp file and returns it as a gtfstk object.
    """
    r = requests.get(url)
    with tempfile.NamedTemporaryFile() as f:
        f.write(r._content)
        f.seek(0)  # https://stackoverflow.com/questions/10478242/temp-readline-empty
        return gtfstk.read_gtfs(f.name, dist_units=dist_units)


def get_rail_stops(gtfs):
    """
    Filters a GTFS object for routes of route_type 0 and returns a unique list of stops.
    """
    rail_stops = []
    for route_id in gtfs.routes[gtfs.routes["route_type"] == 0]["route_id"]:
        for trip_id in gtfs.trips[gtfs.trips["route_id"] == route_id]["trip_id"]:
            for stop_id in gtfs.stop_times[gtfs.stop_times["trip_id"] == trip_id][
                "stop_id"
            ]:
                rail_stops.append(stop_id)
    rail_stops = set(rail_stops)
    return gtfs.stops[gtfs.stops["stop_id"].isin(rail_stops)]


def contour_plot(ax, point, resolution, number):
    x = numpy.linspace(point.x - resolution, point.x + resolution, number)
    y = numpy.linspace(point.y - resolution, point.y + resolution, number)
    url = "http://localhost:5000/table/v1/walking/" + str(point.x) + "," + str(point.y)
    for i in x:
        for j in y:
            url += ";" + str(i) + "," + str(j)
    url += "?sources=0"
    request = requests.get(url)
    durations = request.json()["durations"][0][1:]
    z = numpy.array(durations).reshape([len(x), len(y)])
    ax.contour(x, y, z, levels=[300, 600, 900])


def plot_linestring(foliumMap, row):
    folium.PolyLine(
        locations=zip(row["geometry"].xy[1], row["geometry"].xy[0]), color=row["color"]
    ).add_to(foliumMap)


def plot_stops_with_contour(foliumMap, stops, markercolor):
    """
    * plot_stops(folium.folium.Map: foliumMap, pandas.core.frame.DataFrame: stops, string: markercolor)
    * foliumMap is the map to plot the stops on
    * stops is the DataFrame that contains the stops from url2gtfs().stops or get_rail_stops
    * color is a string of the marker color for the stops
    * Returns pandas.core.series.Series of folium.map.Marker
    * This method requires a OSRM server of the area running on http://localhost:5000
    """
    fig, ax = pyplot.subplots()
    stops.apply(
        lambda row: contour_plot(
            ax, Point(float(row["stop_lon"]), float(row["stop_lat"])), 0.025, 15
        ),
        axis=1,
    )
    geojson = mplleaflet.fig_to_geojson(fig=fig)
    features = geopandas.GeoDataFrame.from_features(geojson["features"])
    features.apply(partial(plot_linestring, foliumMap), axis=1)
    stops.apply(
        lambda row: folium.Marker(
            [row["stop_lat"], row["stop_lon"]],
            popup=row["stop_name"],
            icon=folium.Icon(color=markercolor),
        ).add_to(foliumMap),
        axis=1,
    )


def plot_stops(foliumMap, stops, markercolor):
    stops.apply(
        lambda row: folium.Marker(
            [row["stop_lat"], row["stop_lon"]],
            popup=row["stop_name"],
            icon=folium.Icon(color=markercolor),
        ).add_to(foliumMap),
        axis=1,
    )


def stop_id_to_distance(feed, aea_line, stop_id):
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
        return stop_id_to_distance(feed, aea_line, stop_id)

    for trip_id in trips:
        d = feed.stop_times[feed.stop_times["trip_id"] == trip_id].copy()
        d["arrival_time_object"] = d.arrival_time.map(timestring_to_timeobject)
        d["departure_time_object"] = d.departure_time.map(timestring_to_timeobject)
        d["distance"] = d.stop_id.map(stop_id_to_distance_cached)
        plt.plot(d.arrival_time_object, d.distance / 1000)
    plt.xlabel("Time of Day")
    plt.ylabel("Distance on Route")
    plt.show()
