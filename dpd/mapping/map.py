import folium
import geonetworkx
from matplotlib import pyplot as plt

from dpd.geometry import GeometricDict
from .links import Links


class Map:
    """
    A class for creating a link network map that includes links (made up of lanes) that go between intersections.
    """

    def __init__(self):
        self.intersections = GeometricDict()
        self.links = Links()

    def to_geodigraph(self):
        G = geonetworkx.GeoDiGraph()
        nodes = []
        for index, intersection in self.intersections.items():
            nodes.append((index, intersection))
        G.add_nodes_from(nodes)
        edges = []
        for index, link in self.links.items():
            edges.append(
                (
                    link.input_intersection.name
                    if link.input_intersection
                    else None,
                    link.output_intersection.name
                    if link.output_intersection
                    else None,
                    link,
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
            self.intersections.plot(filter_box, ax=ax, **kwargs)
        if include_links:
            self.links.plot(filter_box, ax=ax, **kwargs)
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
