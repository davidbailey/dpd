import geopandas
from matplotlib import pyplot as plt
import networkx
from shapely.geometry import Point

from dpd.uscensus import get_uscensus_data
from dpd.utils import epsg4326_to_aea
from .centroid_distance_dataframe import CentroidDistanceDataFrame
from .cost_dataframe import CostDataFrame
from .origin_destination_dataframe import OriginDestinationDataFrame


class Zones(geopandas.GeoDataFrame):
    """
    A class to store four-step model zones.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_uscensus(state, year):
        # TODO add a way to specify the level to get the geometry for. e.g. currently we only support census tract, but we may want to do a county-level analysis.
        zones = get_uscensus_data(
            year, state, ["NAME", "B01003_001E", "B08604_001E"], with_geometry=True
        )
        zones["GEOID"] = zones["GEOID"].apply(int)
        zones.set_index("GEOID", inplace=True)
        zones.rename(
            columns={
                "NAME_x": "Name",
                "B01003_001E": "Production",
                "B08604_001E": "Attraction",
            },
            inplace=True,
        )
        return Zones(zones)

    def calculate_aea_geometry(self):
        """
        Calculate an aea_geometry column.
        """
        self["aea_geometry"] = self.geometry.map(
            lambda geometry: epsg4326_to_aea(geometry)
        )

    def calculate_centroids(self):
        """
        Calculate the centroid of each zones.
        """
        self["centroid"] = self.geometry.map(
            lambda geometry: Point(geometry.centroid.y, geometry.centroid.x)
        )

    def calculate_centroid_distance_dataframe(self):
        """
        Calculate a dataframe containing the distance between the centroid of all zones.
        """
        if not "centroid" in self.columns:
            self.calculate_centroids()
        self["aea_centroid"] = self.centroid.to_crs(
            "North America Albers Equal Area Conic"
        )
        return CentroidDistanceDataFrame.from_centroids(self.aea_centroid)

    def calculate_cost_dataframe(self, beta=None, centroid_distance_dataframe=None):
        """
        Calculate a dataframe containing the travel cost between all zones.
        """
        if centroid_distance_dataframe is None:
            centroid_distance_dataframe = self.calculate_centroid_distance_dataframe()
        return CostDataFrame.from_centroid_distance_dataframe(
            centroid_distance_dataframe, beta
        )

    def calculate_origin_destination_dataframe(
        self, beta=None, centroid_distance_dataframe=None, cost_dataframe=None
    ):
        """
        Calculate an origin-destination dataframe.
        """
        if cost_dataframe is None:
            cost_dataframe = self.calculate_cost_dataframe(
                beta=beta, centroid_distance_dataframe=centroid_distance_dataframe
            )
        return OriginDestinationDataFrame.from_ipfn(self, cost_dataframe)

    def build_graph(self, centroid_distance_dataframe=None):
        if centroid_distance_dataframe is None:
            centroid_distance_dataframe = self.calculate_centroid_distance_dataframe()
        self.graph = networkx.Graph()
        self.graph.add_nodes_from(self.index)
        for zone1 in self.index:
            for zone2 in self.index:
                if self.loc[zone1]["geometry"].touches(self.loc[zone2]["geometry"]):
                    self.graph.add_edge(
                        zone1,
                        zone2,
                        distance=centroid_distance_dataframe.loc[zone1][zone2],
                        volume=0.0,
                    )
        return self.graph

    def visualize_route_assignment(self, linewidth=0.0001, ax=None):
        if not self.graph:
            raise AttributeError(
                "Graph not built yet. Please run Zones.buid_graph and OriginDestinationDataFrame.route_assignment() first."
            )
        if not "centroid" in self.columns:
            self["centroid"] = self.geometry.map(
                lambda geometry: Point(geometry.centroid.y, geometry.centroid.x)
            )
        if ax is None:
            ax = plt.subplot(111)
        self.plot(ax=ax)
        for edge in self.graph.edges:
            volume = self.graph.edges[edge]["volume"]
            y = [self.loc[edge[0]]["centroid"].x, self.loc[edge[1]]["centroid"].x]
            x = [self.loc[edge[0]]["centroid"].y, self.loc[edge[1]]["centroid"].y]
            ax.plot(
                x,
                y,
                color="#444444",
                linewidth=volume * linewidth,
                solid_capstyle="round",
                zorder=1,
            )
