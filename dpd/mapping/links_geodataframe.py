from geopandas import GeoDataFrame


class LinksGeoDataFrame(GeoDataFrame):
    def pyrosm_assumed_lanes(row):
        pass

    def pyrosm_assumed_speed(row):
        pass

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
        network["assumed_lanes"] = network.apply(self.pyrosm_assumed_lanes, axis=1)
        network["assumed_speed"] = network.apply(self.pyrosm_assumed_speed, axis=1)
        return LinksGeoDataFrame(network)
