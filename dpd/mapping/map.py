import folium
import geonetworkx
import geopandas as gpd
from matplotlib import pyplot as plt
from pyproj import CRS
from shapely.geometry import box

from .intersection import Intersection
from .lane import Lane
from .road import Road


class Map:
    """
    A class for creating a road network map that includes roads (made up of lanes) that go between intersections.
    """

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

    def transform_intersections_to_aea(self):
        aea = CRS.from_string("North America Albers Equal Area Conic")
        self.intersections.to_crs(aea, inplace=True)
        for _, intersection in self.intersections.iterrows():
            intersection["Intersection"].geometry = intersection["geometry"]

    def transform_intersections_to_epsg4326(self):
        self.intersections.to_crs("EPSG:4326", inplace=True)
        for _, intersection in self.intersections.iterrows():
            intersection["Intersection"].geometry = intersection["geometry"]

    def transform_roads_to_aea(self):
        aea = CRS.from_string("North America Albers Equal Area Conic")
        self.roads.to_crs(aea, inplace=True)
        for _, road in self.roads.iterrows():
            road["Road"].geometry = road["geometry"]

    def transform_roads_to_epsg4326(self):
        self.roads.to_crs("EPSG:4326", inplace=True)
        for _, road in self.roads.iterrows():
            road["Road"].geometry = road["geometry"]

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


    def plot_folium_df(self, folium_map, df, filter_df, fields):
            df.crs = "EPSG:4326"
            if filter_df:
                plot_df = gpd.overlay(df, filter_df, how='intersection')
            else:
                plot_df = df
            if fields:
                geojson = folium.GeoJson(
                    plot_df[["geometry"]],
                    tooltip=folium.features.GeoJsonTooltip(fields=fields),
                )
            else:
                geojson = folium.GeoJson(plot_df[["geometry"]])
            geojson.add_to(folium_map)
        

    def plot_folium(
        self,
        include_intersections=False,
        include_roads=True,
        folium_map=None,
        fields_intersections=None,
        fields_roads=None,
        filter_box=None
    ):
        if not folium_map:
            folium_map = folium.Map(location=(38.9, -77), zoom_start=12)
        if filter_box:
            filter_df = GeoDataFrame(Polygon(box(filter_box)), columns=["geometry"])
            filter_df = "EPSG:4326"
        if include_roads:
            self.plot_folium_df(folium_map, self.roads, filter_df, fields_roads)
        if include_intersections:
            self.plot_folium_df(folium_map, self.intersections, filter_df, fields_intersections)
        return folium_map

    def to_geodigraph(self):
        G = geonetworkx.GeoDiGraph()
        nodes = []
        for index, intersection in self.intersections.iterrows():
            nodes.append((index, intersection.to_dict()))
        G.add_nodes_from(nodes)
        edges = []
        for index, road in self.roads.iterrows():
            edges.append(
                (
                    road["Road"].input_intersection.name
                    if road["Road"].input_intersection
                    else None,
                    road["Road"].output_intersection.name
                    if road["Road"].output_intersection
                    else None,
                    road.to_dict(),
                )
            )
        G.add_edges_from(edges)
        return G
