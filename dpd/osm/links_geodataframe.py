from geopandas import GeoDataFrame
from pyrosm import OSM, get_data

class LinksGeoDataFrame(GeoDataFrame):
    def from_pyrosm_region(region):
        fp = get_data(region)
        osm = OSM(fp)
        network = osm.get_network(
            "all",
            extra_attributes=[
                "lanes:forward",
                "lanes:backward",
                "cycleway:left",
                "cycleway:right",
            ],
        )
        return LinksGeoDataFrame(network)
