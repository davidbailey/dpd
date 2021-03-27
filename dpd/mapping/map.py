import folium
import geonetworkx
import geopandas as gpd
from matplotlib import pyplot as plt
from pyproj import CRS
from shapely.geometry import box


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

    def plot_df(self, ax, df, filter_df):
        df.plot(ax=ax)
        for idx, row in df.iterrows():
            plt.annotate(
                text=idx,
                xy=row.geometry.centroid.coords[0],
                horizontalalignment="center",
            )

    def plot(self, include_intersections=False, include_roads=True, filter_box=None):
        fig = plt.figure(figsize=(18, 16))
        ax = fig.add_subplot(111)
        if filter_box:
            filter_df = GeoDataFrame(Polygon(box(filter_box)), columns=["geometry"])
            filter_df = "EPSG:4326"
        else:
            filter_df = None
        if include_intersections:
            self.plot_df(ax, self.intersections, filter_df)
        if include_roads:
            self.plot_df(ax, self.roads, filter_df)
        plt.show()

    def plot_folium_df(self, folium_map, df, filter_df, **kwargs):
        if filter_df:
            plot_df = gpd.overlay(df, filter_df, how="intersection")
        else:
            plot_df = df
        geojson = folium.GeoJson(plot_df.to_json(), **kwargs)
        geojson.add_to(folium_map)

    def plot_folium(
        self,
        include_intersections=False,
        include_roads=True,
        folium_map=None,
        filter_box=None,
    ):
        if not folium_map:
            folium_map = folium.Map(location=(38.9, -77), zoom_start=12)
        if filter_box:
            filter_df = GeoDataFrame(Polygon(box(filter_box)), columns=["geometry"])
            filter_df.crs = "EPSG:4326"
        else:
            filter_df = None
        if include_roads:
            if not "number_of_lanes" in self.roads.columns:
                self.roads["number_of_lanes"] = self.roads["Road"].map(
                    lambda road: len(road.lanes)
                )
            style_function = lambda x: {"weight": x["properties"]["number_of_lanes"]}
            self.plot_folium_df(
                folium_map,
                self.roads[["geometry", "number_of_lanes"]],
                filter_df,
                style_function=style_function,
            )
        if include_intersections:
            if not "name" in self.intersections.columns:
                self.intersections["name"] = self.intersections["Intersection"].map(
                    lambda intersection: intersection.name
                )
            tooltip = (folium.features.GeoJsonTooltip(fields=["name"]),)
            self.plot_folium_df(
                folium_map,
                self.intersections[["geometry", "name"]],
                filter_df,
                tooltip=tooltip,
            )
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
