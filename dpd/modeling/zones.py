from functools import partial

import networkx
from astropy.units import m
from geopandas import GeoDataFrame
from matplotlib import pyplot as plt
from shapely.geometry import Point
from tobler.area_weighted import area_interpolate
from tobler.util import h3fy

from dpd.analysis.units import person
from dpd.shapely import uniform_points_in_polygon
from dpd.uscensus import get_uscensus_data

from .distance_dataframe import DistanceDataFrame
from .trip_dataframe import TripDataFrame


class Zones(GeoDataFrame):
    """
    A class to store four-step model zones.

    * Index is an identifier
    * Columns are Geometry (Polygons), Production, Attraction
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def h3fy_area_interpolated(self, h3fy_kwds=None, area_interpolate_kwds=None):
        if h3fy_kwds is None:
            h3fy_kwds = {}
        if area_interpolate_kwds is None:
            area_interpolate_kwds = {}
        h3fy_zones = h3fy(self, **h3fy_kwds)
        area_interpolate_zones = area_interpolate(
            source_df=self, target_df=h3fy_zones, **area_interpolate_kwds
        )
        return Zones(area_interpolate_zones)

    @staticmethod
    def from_uscensus(state, year, include_units=False):
        # TODO add a way to specify the level to get the geometry for. e.g. currently we only support census tract, but we may want to do a county-level analysis.
        zones = get_uscensus_data(
            year, state, ["NAME", "B01003_001E", "B08604_001E"], with_geometry=True
        )
        zones["GEOID"] = zones["GEOID"].apply(int)
        zones.set_index("GEOID", inplace=True)
        zones.rename(
            columns={
                "NAME_x": "Name",
                "B01003_001E": "Total Population",
                "B08604_001E": "Worker Population",
            },
            inplace=True,
        )
        zones["Total Population"] = zones["Total Population"].fillna(0).apply(int)
        zones["Worker Population"] = zones["Worker Population"].fillna(0).apply(int)
        if include_units:
            zones["Total Population"] = zones["Total Population"].map(
                lambda x: x * person
            )
            zones["Worker Population"] = zones["Worker Population"].map(
                lambda x: x * person
            )
            zones["ALAND"] = zones["ALAND"].map(lambda x: x * m**2)
            zones["AWATER"] = zones["AWATER"].map(lambda x: x * m**2)
        zones["Total Population + Worker Population"] = (
            zones["Total Population"] + zones["Worker Population"]
        )
        zones["Total Population Density"] = zones["Total Population"] / zones["ALAND"]
        zones["Worker Population Density"] = zones["Worker Population"] / zones["ALAND"]
        zones["Total Population + Worker Population Density"] = (
            zones["Total Population + Worker Population"] / zones["ALAND"]
        )
        return Zones(zones)

    def calculate_distance_dataframe(self, method="haversine"):
        """
        Calculate a dataframe containing the distance between the centroid of all zones.
        """
        centroids = self.geometry.map(
            lambda geometry: Point(geometry.centroid.y, geometry.centroid.x)
        )
        return DistanceDataFrame.from_origins_destinations(
            centroids, centroids, method=method
        )

    def calculate_trip_dataframe_from_ipfn(self, distance_dataframe=None):
        """
        Calculate an trip dataframe using IPFN.
        """
        if distance_dataframe is None:
            distance_dataframe = self.calculate_distance_dataframe()
        return TripDataFrame.from_ipfn(self, distance_dataframe)

    def production_attraction_from_lodes(
        self, origin_destination_dataframe, column="S000"
    ):
        self["Total Population"] = origin_destination_dataframe.groupby("trct_h").sum()[
            column
        ]
        self["Worker Population"] = origin_destination_dataframe.groupby(
            "trct_w"
        ).sum()[column]
        zones["Total Population + Worker Population"] = (
            zones["Total Population"] + zones["Worker Population"]
        )
        zones["Total Population Density"] = zones["Total Population"] / zones["ALAND"]
        zones["Worker Population Density"] = zones["Worker Population"] / zones["ALAND"]
        zones["Total Population + Worker Population Density"] = (
            zones["Total Population + Worker Population"] / zones["ALAND"]
        )
        return Zones(self)

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
        if "centroid" not in self.columns:
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

    def polygons_to_points(self, num=10):
        if "WGS 84" not in self.crs.name:
            raise ValueError(
                "CRS does not contain WGS 84. Results will not be accurate"
            )
        points = self.geometry.map(partial(uniform_points_in_polygon, num=num))
        num_points_in_polygon = points.map(len)
        production = self["Total Population"] / num_points_in_polygon
        attraction = self["Worker Population"] / num_points_in_polygon
        production_attraction_sum = (
            self["Total Population + Worker Population"] / num_points_in_polygon
        )
        data = []
        for index in points.index:
            for point in points[index]:
                data.append(
                    {
                        "GEOID": index,
                        "geometry": point,
                        "Total Population": production[index],
                        "Worker Population": attraction[index],
                        "Total Population + Worker Population": production_attraction_sum[
                            index
                        ],
                    }
                )
        return GeoDataFrame(data=data, crs=self.crs)
