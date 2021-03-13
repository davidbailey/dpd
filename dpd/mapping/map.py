import folium
import geopandas as gpd
from matplotlib import pyplot as plt

from .intersection import Intersection
from .lane import Lane
from .road import Road


class Map:
    def __init__(self):
        self.intersections = gpd.GeoDataFrame(columns=["geometry", "Intersection"])
        self.roads = gpd.GeoDataFrame(columns=["geometry", "Road"])

    def add_intersection(self, intersection):
        self.intersections.loc[intersection.name] = [
            intersection.geometry,
            intersection,
        ]

    def add_road(self, road):
        self.roads.loc[road.name] = [road.geometry, road]

    def plot(self, include_intersections=False, include_roads=True, fig=None, ax=None):
        if not fig:
            fig = plt.figure(figsize=(18, 16))
        if not ax:
            ax = fig.add_subplot(111)
        if include_intersections:
            self.intersections.plot(ax=ax)
            for idx, row in self.intersections.iterrows():
                plt.annotate(
                    text=idx,
                    xy=row.geometry.centroid.coords[0],
                    horizontalalignment="center",
                )
        if include_roads:
            self.roads.plot(ax=ax)
            for idx, row in self.roads.iterrows():
                plt.annotate(
                    text=idx,
                    xy=row.geometry.centroid.coords[0],
                    horizontalalignment="center",
                )
        plt.show()

    def plot_folium(
        self, include_intersections=False, include_roads=True, folium_map=None
    ):
        if not folium_map:
            folium_map = folium.Map(location=(38.9, -77), zoom_start=12)
        if include_intersections:
            self.intersections.crs = "EPSG:4326"
            geojson = folium.GeoJson(
                self.intersections[["geometry"]],
                # tooltip=folium.features.GeoJsonTooltip(
                # fields=['index'],
                # )
            )
            geojson.add_to(folium_map)
        if include_roads:
            self.roads.crs = "EPSG:4326"
            geojson = folium.GeoJson(
                self.roads[["geometry"]],
                # tooltip=folium.features.GeoJsonTooltip(
                # fields=['index'],
                # )
            )
            geojson.add_to(folium_map)
        return folium_map
