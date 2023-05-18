from ipfn import ipfn
import networkx
from numpy import outer, exp
import pandas

from dpd.osrm import route
from dpd.uscensus import download_lodes_data, download_lodes_xwalk
from dpd.shapely import random_point_in_polygon


class TripDataFrame(pandas.DataFrame):
    """
    A class to store an origin-destination matrix for the trip distribution step of a four-step model. Index defines origins. Columns define destinations.
    """


    @staticmethod
    def from_gravity_model(origin_population, destination_population, distance_dataframe, function="inverse", G=1, a=1, b=1, d=1, *args, **kwargs):
        if function == "inverse":
            trip_array = G * outer((origin_population**a), (destination_population**b)) / distance_dataframe**d
        elif function == "exponential":
            trip_array = G * outer((origin_population**a), (destination_population**b)) * exp(-d * distance_dataframe)
        else:
            raise NotImplementedError("Function %s not implemented" % (function))
        return TripDataFrame(data=trip_array, index=origin_population.index, columns=destination_population.index, *args, **kwargs)
                    
    @staticmethod
    def from_ipfn(zones, cost_dataframe, *args, **kwargs):
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
        return TripDataFrame(
            trips.pivot(
                index="origin_zone", columns="destination_zone", values="total",
                *args, **kwargs
            ).stack()
        )

    @staticmethod
    def from_lodes(st, year, *args, **kwargs):
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
        return TripDataFrame(od_xwalk, *args, **kwargs)

    def add_geometry_from_zones(self, zones, method=random_point_in_polygon):
        (self["home_geometry"], self["work_geometry"]) = list(
            map(
                list,
                zip(
                    *self.index.map(
                        lambda index: [
                            method(zones.loc[index[1]]["geometry"]),
                            method(zones.loc[index[0]]["geometry"]),
                        ]
                    )
                ),
            )
        )

    def route_assignment(self, zones, column="S000"):
        for (origin, destination), row in self.iterrows():
            path = networkx.shortest_path(zones.graph, origin, destination)
            # TODO this fails when there is no path (e.g. islands). But these people still get to work somehow.
            for i in range(len(path) - 1):
                zones.graph[path[i]][path[i + 1]]["volume"] = (
                    zones.graph[path[i]][path[i + 1]]["volume"] + row[column]
                )
        return zones.graph

    def add_route_hw_from_osrm(self, url_base, mode):
        # check if home and work exist, if not, create them
        if "home_geometry" not in self.columns and "work_geometry" in self.columns:
            raise RuntimeError(
                "No home_geometry and/or work_geometry. Please run add_geometry_from_zones first"
            )
        self["routes"] = self.apply(
            lambda row: route(
                row["home_geometry"], row["work_geometry"], url_base, mode
            )["routes"],
            axis=1,
        )
