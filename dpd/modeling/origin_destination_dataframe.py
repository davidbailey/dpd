from ipfn import ipfn
import networkx
import pandas

from dpd.uscensus import download_lodes_data, download_lodes_xwalk


class OriginDestinationDataFrame(pandas.DataFrame):
    """
    A class to store an origin-destination matrix for the trip distribution step of a four-step model. Index defines origins. Columns define destinations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_ipfn(zones, cost_dataframe):
        # TODO fix this method
        cost_dataframe["origin_zone"] = cost_dataframe.index
        cost_dataframe = cost_dataframe.melt(id_vars=["origin_zone"])
        cost_dataframe.columns = ["origin_zone", "destination_zone", "total"]
        production = zones["Production"]
        production.index.name = "origin_zone"
        attraction = zones["Attraction"]
        attraction.index.name = "destination_zone"
        aggregates = [production, attraction]
        dimensions = [["origin_zone"], ["destination_zone"]]
        IPF = ipfn.ipfn(cost_dataframe, aggregates, dimensions)
        trips = IPF.iteration()
        return OriginDestinationDataFrame(
            trips.pivot(
                index="origin_zone", columns="destination_zone", values="total"
            ).stack()
        )

    @staticmethod
    def from_lodes(st, year):
        od = pandas.read_csv(download_lodes_data("od", st, "main", "JT00", year))
        xwalk = pandas.read_csv(download_lodes_xwalk(st))
        xwalk.set_index("tabblk2010", inplace=True)
        od_xwalk = pandas.merge(
            od, xwalk[["trct"]], left_on="w_geocode", right_index=True
        )
        od_xwalk = pandas.merge(
            od_xwalk,
            xwalk[["trct"]],
            left_on="h_geocode",
            right_index=True,
            suffixes=("_w", "_h"),
        )
        od_xwalk = od_xwalk.groupby(["trct_w", "trct_h"]).sum()
        return OriginDestinationDataFrame(od_xwalk)

    def route_assignment(self, zones, column="S000"):
        for (origin, destination), row in self.iterrows():
            path = networkx.shortest_path(zones.graph, origin, destination)
            # TODO this fails when there is no path (e.g. islands). But these people still get to work somehow.
            for i in range(len(path) - 1):
                zones.graph[path[i]][path[i + 1]]["volume"] = (
                    zones.graph[path[i]][path[i + 1]]["volume"] + row["S000"]
                )
        return zones.graph
