from astropy import units
import folium
import geopandas
from matplotlib import pyplot as plt
import networkx
from pandas import DataFrame
from pyproj import CRS
from shapely.geometry import Point
from tqdm import tqdm

from dpd.shapely import uniform_points_in_polygon
from dpd.uscensus import get_uscensus_data
from .centroid_distance_dataframe import CentroidDistanceDataFrame
from .cost_dataframe import CostDataFrame
from .origin_destination_dataframe import OriginDestinationDataFrame


class Zones(geopandas.GeoDataFrame):
    """
    A class to store four-step model zones.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Production = self.Production.fillna(0).apply(int)
        self.Attraction = self.Attraction.fillna(0).apply(int)
        self["ProductionAttractionSum"] = self.Production + self.Attraction
        self["Production Density"] = self.Production / self.ALAND * 1000000
        self["Attraction Density"] = self.Attraction / self.ALAND * 1000000
        self["ProductionAttractionSum Density"] = self.ProductionAttractionSum / self.ALAND * 1000000

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

    def calculate_centroid_distance_dataframe(self):
        """
        Calculate a dataframe containing the distance between the centroid of all zones.
        """
        self.to_crs(CRS.from_string("North America Albers Equal Area Conic"))
        self["aea_centroid"] = self.geometry.map(
            lambda geometry: Point(geometry.centroid.y, geometry.centroid.x)
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

    def production_attraction_from_lodes(self, origin_destination_dataframe, column="S000"):
        self["Production"] = origin_destination_dataframe.groupby("trct_h").sum()[column]
        self["Attraction"] = origin_destination_dataframe.groupby("trct_w").sum()[column]
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

    def accessibility_zone(self, zone, route, mode):
        points = uniform_points_in_polygon(zone.geometry)
        return route.accessibility(points, mode)

    def accessibility(
        self,
        route,
        time=15 * units.minute,
        mode="walking",
        production_or_attraction="Production",
    ):
        stops_dict = route.stops_dict
        stops_dict.to_crs("North America Albers Equal Area Conic")
        for stop in stops_dict:
            stops_dict[stop].geometry = stops_dict[stop].accessibility_radius(
                time, mode
            )
        stops_dict.to_crs(CRS.from_epsg(4326))
        self.to_crs(CRS.from_epsg(4326), inplace=True)
        indices = []
        for index, row in self.iterrows():
            for stop in stops_dict:
                if row.geometry.intersection(stops_dict[stop].geometry).area > 0:
                    indices.append(index)
        self.to_crs("North America Albers Equal Area Conic", inplace=True)
        accessibility = []
        for zone_index, zone in tqdm(
            self.filter(indices, axis=0).iterrows(), total=len(indices)
        ):
            accessibility_zone = self.accessibility_zone(zone, route, mode)
            accessibility_zone["accessibility"] = accessibility_zone[
                "accessibility"
            ].map(lambda x: x.value)
            accessibility_zone_min = accessibility_zone.loc[
                accessibility_zone.groupby(["x", "y"])["accessibility"].idxmin()
            ]
            for stop_index, row in accessibility_zone_min.iterrows():
                accessibility.append(
                    {
                        "zone": zone_index,
                        "stop": stop_index[2],
                        "time": row["accessibility"],
                        "population": zone[production_or_attraction]
                        / len(accessibility_zone),
                    }
                )
        return DataFrame(accessibility)

    def plot_density(self, folium_map, production_or_attraction="Production", *args, **kwargs):
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
