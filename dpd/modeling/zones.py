import geopandas
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

    def calculate_centroid_distance_dataframe(self):
        """
        Calculate a dataframe containing the distance between the centroid of all zones.
        """
        return CentroidDistanceDataFrame.from_geometries(self.geometry)

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
