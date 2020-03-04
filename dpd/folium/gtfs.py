from functools import partial

import folium
import geopandas
from matplotlib import pyplot
import mplleaflet
from shapely.geometry import Point

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
