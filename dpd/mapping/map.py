import folium
import geonetworkx
import geopandas as gpd
from matplotlib import pyplot as plt
from pyproj import CRS
from shapely.geometry import box, Polygon, LineString


class Map:
    """
    A class for creating a link network map that includes links (made up of lanes) that go between intersections.
    """

    def __init__(self):
        self.intersections = gpd.GeoDataFrame(columns=["geometry", "Intersection"])
        self.links = gpd.GeoDataFrame(columns=["geometry", "Link"])

    def add_intersection(self, intersection):
        self.intersections.loc[intersection.name] = [
            intersection.geometry,
            intersection,
        ]

    def add_link(self, link):
        self.links.loc[link.name] = [link.geometry, link]

    def transform_intersections_to_aea(self):
        aea = CRS.from_string("North America Albers Equal Area Conic")
        self.intersections.to_crs(aea, inplace=True)
        for _, intersection in self.intersections.iterrows():
            intersection["Intersection"].geometry = intersection["geometry"]

    def transform_intersections_to_epsg4326(self):
        self.intersections.to_crs("EPSG:4326", inplace=True)
        for _, intersection in self.intersections.iterrows():
            intersection["Intersection"].geometry = intersection["geometry"]

    def transform_links_to_aea(self):
        aea = CRS.from_string("North America Albers Equal Area Conic")
        self.links.to_crs(aea, inplace=True)
        for _, link in self.links.iterrows():
            link["Link"].geometry = link["geometry"]

    def transform_links_to_epsg4326(self):
        self.links.to_crs("EPSG:4326", inplace=True)
        for _, link in self.links.iterrows():
            link["Link"].geometry = link["geometry"]

    def plot_df(self, ax, df, filter_df):
        df.plot(ax=ax)
        for idx, row in df.iterrows():
            plt.annotate(
                text=idx,
                xy=row.geometry.centroid.coords[0],
                horizontalalignment="center",
            )

    def plot(self, include_intersections=False, include_links=True, filter_box=None):
        fig = plt.figure(figsize=(18, 16))
        ax = fig.add_subplot(111)
        if filter_box:
            filter_df = gpd.GeoDataFrame(
                [
                    Polygon(
                        box(filter_box[0], filter_box[1], filter_box[2], filter_box[3])
                    )
                ],
                columns=["geometry"],
            )
            filter_df = "EPSG:4326"
        else:
            filter_df = None
        if include_intersections:
            self.plot_df(ax, self.intersections, filter_df)
        if include_links:
            self.plot_df(ax, self.links, filter_df)
        plt.show()

    def plot_folium_df(self, folium_map, df, filter_df, **kwargs):
        if filter_df is not None:
            plot_df = gpd.overlay(df, filter_df, how="intersection")
            plot_df = plot_df[plot_df["geometry"] != LineString()]
        else:
            plot_df = df
        geojson = folium.GeoJson(plot_df.to_json(), **kwargs)
        geojson.add_to(folium_map)

    def plot_folium(
        self,
        include_intersections=False,
        include_links=True,
        folium_map=None,
        filter_box=None,
    ):
        if not folium_map:
            folium_map = folium.Map(location=(38.9, -77), zoom_start=12)
        if filter_box:
            filter_df = gpd.GeoDataFrame(
                [
                    Polygon(
                        box(filter_box[0], filter_box[1], filter_box[2], filter_box[3])
                    )
                ],
                columns=["geometry"],
            )
            filter_df.crs = "EPSG:4326"
        else:
            filter_df = None
        if include_links:
            if not "number_of_segments" in self.links.columns:
                self.links["number_of_segments"] = self.links["Link"].map(
                    lambda link: len(link.segments) - 2
                )
            style_function = lambda x: {"weight": x["properties"]["number_of_segments"]}
            if not "name" in self.links.columns:
                self.links["name"] = self.links["Link"].map(lambda link: link.name)
            if not "segments" in self.links.columns:
                self.links["segments"] = self.links["Link"].map(
                    lambda link: str(list(map(type, link.segments)))
                )
            tooltip = folium.features.GeoJsonTooltip(fields=["name", "segments"])
            self.plot_folium_df(
                folium_map,
                self.links[["geometry", "name", "number_of_segments", "segments"]],
                filter_df,
                style_function=style_function,
                tooltip=tooltip,
            )
        if include_intersections:
            if not "name" in self.intersections.columns:
                self.intersections["name"] = self.intersections["Intersection"].map(
                    lambda intersection: intersection.name
                )
            tooltip = folium.features.GeoJsonTooltip(fields=["name"])
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
        for index, link in self.links.iterrows():
            edges.append(
                (
                    link["Link"].input_intersection.name
                    if link["Link"].input_intersection
                    else None,
                    link["Link"].output_intersection.name
                    if link["Link"].output_intersection
                    else None,
                    link.to_dict(),
                )
            )
        G.add_edges_from(edges)
        return G
