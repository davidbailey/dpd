from geopandas import GeoDataFrame


class LinksGeoDataFrame(GeoDataFrame):
    def from_pyrosm(osm):
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
