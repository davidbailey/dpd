from functools import partial

import folium
from geopandas import GeoDataFrame
from matplotlib import pyplot as plt
import networkx
from pyproj import CRS
from shapely.geometry import Point

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
        self.Production = self.Production.fillna(0).apply(int)
        self.Attraction = self.Attraction.fillna(0).apply(int)
        self["ProductionAttractionSum"] = self.Production + self.Attraction
        self["Production Density"] = self.Production / self.ALAND * 1000000
        self["Attraction Density"] = self.Attraction / self.ALAND * 1000000
        self["ProductionAttractionSum Density"] = (
            self.ProductionAttractionSum / self.ALAND * 1000000
        )

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
        zones["Production"] = zones.Production.apply(int)
        zones["Attraction"] = 0
        return Zones(zones)

    def calculate_distance_dataframe(self):
        """
        Calculate a dataframe containing the distance between the centroid of all zones.
        """
        centroids = self.geometry.map(
            lambda geometry: Point(geometry.centroid.y, geometry.centroid.x)
        )
        return DistanceDataFrame.from_origins_destinations(
            centroids, centroids, method="haversine"
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
        self["Production"] = origin_destination_dataframe.groupby("trct_h").sum()[
            column
        ]
        self["Attraction"] = origin_destination_dataframe.groupby("trct_w").sum()[
            column
        ]
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
        if "Albers_Equal_Area_Conic" not in self.crs.name:
            raise ValueError(
                "CRS does not contain Albers_Equal_Area_Conic. Results will not be accurate"
            )
        points = self.geometry.map(partial(uniform_points_in_polygon, num=num))
        num_points_in_polygon = points.map(len)
        production = self["Production"] / num_points_in_polygon
        attraction = self["Attraction"] / num_points_in_polygon
        production_attraction_sum = (
            self["ProductionAttractionSum"] / num_points_in_polygon
        )
        data = []
        for index in points.index:
            for point in points[index]:
                data.append(
                    {
                        "GEOID": index,
                        "geometry": point,
                        "Production": production[index],
                        "Attraction": attraction[index],
                        "ProductionAttractionSum": production_attraction_sum[index],
                    }
                )
        return GeoDataFrame(data=data, crs=self.crs)

    def plot_density(
        self, folium_map, production_or_attraction="Production", *args, **kwargs
    ):
        self.to_crs(CRS.from_epsg(4326), inplace=True)
        folium.Choropleth(
            geo_data=self.to_json(),
            data=self,
            columns=[production_or_attraction, production_or_attraction + " Density"],
            key_on="feature.properties." + production_or_attraction,
            fill_color="OrRd",
            nan_fill_color="white",
            fill_opacity=0.7,
            line_opacity=0.2,
            threshold_scale=[
                0,
                2500,
                5000,
                7500,
                10000,
                12500,
                self[production_or_attraction + " Density"].max(),
            ],
            legend_name=production_or_attraction + " density (people/square kilometer)",
            *args,
            **kwargs
        ).add_to(folium_map)
