import folium
import geonetworkx
from matplotlib import pyplot as plt
from pyproj import CRS

from .intersections import Intersections
from .links import Links


class Map:
    """
    A class for creating a link network map that includes links (made up of lanes) that go between intersections.
    """

    def __init__(self):
        self.intersections = Intersections()
        self.links = Links()

    def add_intersection(self, intersection):
        self.intersections.loc[intersection.name] = [
            intersection.geometry,
            intersection,
        ]

    def add_link(self, link):
        self.links.loc[link.name] = [link.geometry, link]

    def transform_intersections_to_aea(
        self,
    ):  # Let's remove these four functions once nothing references them
        aea = CRS.from_string("North America Albers Equal Area Conic")
        self.intersections.transform_crs(aea)

    def transform_intersections_to_epsg4326(self):
        self.intersections.transform_crs("EPSG:4326")

    def transform_links_to_aea(self):
        aea = CRS.from_string("North America Albers Equal Area Conic")
        self.links.transform_crs(aea)

    def transform_links_to_epsg4326(self):
        self.links.transform_crs("EPSG:4326")

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
                    link["object"].input_intersection.name
                    if link["object"].input_intersection
                    else None,
                    link["object"].output_intersection.name
                    if link["object"].output_intersection
                    else None,
                    link.to_dict(),
                )
            )
        G.add_edges_from(edges)
        return G

    def plot(
        self, include_intersections=False, include_links=True, filter_box=None, **kwargs
    ):
        fig = plt.figure(figsize=(18, 16))
        ax = fig.add_subplot(111)
        if include_intersections:
            self.intersections.plot_with_labels(ax, filter_box, **kwargs)
        if include_links:
            self.links.plot_with_labels(ax, filter_box, **kwargs)
        plt.show()

    def plot_folium(
        self, include_intersections=False, include_links=True, filter_box=None, **kwargs
    ):
        folium_map = folium.Map(location=(38.9, -77), zoom_start=12)
        if include_links:
            self.links.plot_folium(folium_map, filter_box, **kwargs)
        if include_intersections:
            self.intersections.plot_folium(folium_map, filter_box, **kwargs)
        return folium_map
