from functools import partial

import folium
import geopandas
from matplotlib import pyplot as plt
import mplleaflet
from shapely.geometry import Point

from dpd.osrm import contour_plot


def _plot_linestring(foliumMap, row):
    folium.PolyLine(
        locations=zip(row["geometry"].xy[1], row["geometry"].xy[0]), color=row["color"]
    ).add_to(foliumMap)


def plot_stops(foliumMap, stops, markercolor="red", with_contour=False, mode="walking"):
    """
    Plot a table of stops on a Folium map.
    
    Args:
        foliumMap (folium.folium.Map): the map to plot the stops on
        stops (pandas.DataFrame): the DataFrame that contains the stops to plot
        color (str): marker color for the stops
        with_contour (bool): if the stops should include a contour_plot representing walk times
    """
    if with_contour:
        fig, ax = plt.subplots()
        stops.apply(
            lambda row: contour_plot(
                ax, Point(float(row["stop_lon"]), float(row["stop_lat"])), 0.025, 15, mode=mode
            ),
            axis=1,
        )
        geojson = mplleaflet.fig_to_geojson(fig=fig)
        features = geopandas.GeoDataFrame.from_features(geojson["features"])
        features.apply(partial(_plot_linestring, foliumMap), axis=1)
    stops.apply(
        lambda row: folium.Marker(
            [row["stop_lat"], row["stop_lon"]],
            popup=row["stop_name"],
            icon=folium.Icon(color=markercolor),
        ).add_to(foliumMap),
        axis=1,
    )
