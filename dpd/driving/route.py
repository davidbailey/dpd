import folium
import geopandas
import numpy as np
from shapely.geometry import LineString, Point
from shapely.ops import linemerge

from dpd.geometry import radius_of_curvature
from dpd.utils import epsg4326_to_aea


class Route(geopandas.GeoDataFrame):
    """
    A way to keep track of all the points that make up a route. We can then calculate their radius of curvature and their speed limit. Then we can have a vehicle drive the route to give us an idea of travel time.
    """

    def __init__(
        self,
        way,
        stops=[],
        tolerance=None,
        max_cant=0.1524,
        max_cant_deficiency=0.075,
        gague=1.435,
        dwell_time=45,
    ):
        """
        Args:
            way (shapely.geometry.LineString): a LineString that contains the route the vehicle follows in EPSG:4326
            stops ([{"geo": shapely.geometry.Point, "name": str}]): a list of "stops" that have a name and a geometry
            tolerance (int): the minimum distance (in meters) for which to keep neighboring stops so they do not create unrealistic curves
            max_cant: (float): the maximum allowable cant (in meters)
            max_cant_deficiency (float): the maximum allowable cant deficiency (in meters)
            gague (float): the track gague (in meters)
            dwell_time (int): the dwell time for each stop (in seconds)

        Returns:
            dpd.driving.Route: a route table 
        """
        aea_way = epsg4326_to_aea(way)
        index = list(map(str, zip(way.xy[0], way.xy[1])))
        geometry = list(map(Point, zip(aea_way.xy[0], aea_way.xy[1])))
        super().__init__(geometry, columns=["geometry"], index=index)
        self.crs = "North America Albers Equal Area Conic"
        self["stop_name"] = ""
        for stop in stops:
            self.at[stop["geo"], "stop_name"] = stop["name"]
        self["after_geometry"] = self["geometry"].shift(-1)
        self["distance_to_next_point"] = self.apply(
            lambda row: None
            if not row["after_geometry"]
            else LineString([row["geometry"], row["after_geometry"]]).length,
            axis=1,
        )
        if (
            tolerance
        ):  # not perfect (e.g. it is possible we will compeltely remove a segment where there are many close points and we really wanted to keep one or two)
            self.drop(
                self[
                    (self["distance_to_next_point"] < tolerance)
                    & (self["stop_name"] == "")
                ].index,
                inplace=True,
            )
            self["after_geometry"] = self["geometry"].shift(-1)
            self["distance_to_next_point"] = self.apply(
                lambda row: None
                if not row["after_geometry"]
                else LineString([row["geometry"], row["after_geometry"]]).length,
                axis=1,
            )
        self["before_geometry"] = self["geometry"].shift(1)
        self["radius_of_curvature"] = self.apply(
            lambda row: 5000
            if row["before_geometry"] is None or row["after_geometry"] is None
            else radius_of_curvature(
                (row["before_geometry"].x, row["before_geometry"].y),
                (row["geometry"].x, row["geometry"].y),
                (row["after_geometry"].x, row["after_geometry"].y),
            ),
            axis=1,
        )
        self["speed_limit"] = self["radius_of_curvature"].apply(
            lambda radius_of_curvature: np.sqrt(
                9.8 * (max_cant + max_cant_deficiency) * radius_of_curvature / gague
            )
        )
        self.max_cant: float = max_cant
        self.max_cant_deficiency: float = max_cant_deficiency
        self.gague: float = gague
        self["dwell_time"] = self.apply(
            lambda row: 0 if row["stop_name"] == "" else dwell_time, axis=1
        )

    def from_osm(osm, relation, *args, **kwargs):
        """
        A way to build a route from OpenStreetMaps data
        
        Args:
            osm (dpd.OSM.osm): the osm that contains the route as a relation
            relation (int): the relation to build a route for
        Returns:
            dpd.driving.Route: a route table 
        """

        ways = [
            osm.ways[member["ref"]].geo
            for member in osm.relations[relation]["members"]
            if member["type"] == "way" and member["role"] == ""
        ]
        way = linemerge(ways)
        stops = []
        for member in osm.relations[relation]["members"]:
            if member["type"] == "node":
                stops.append(
                    {
                        "geo": str(
                            (
                                osm.nodes[member["ref"]].geo.xy[0][0],
                                osm.nodes[member["ref"]].geo.xy[1][0],
                            )
                        ),
                        "name": osm.nodes[member["ref"]].osm["tags"]["name"],
                    }
                )
        return Route(way, stops, *args, **kwargs)

    def add_vehicle(self, vehicle, buffer=0.0):
        """
        A way to have a vehicle "drive" along a route to generate the time between stops
        
        Args:
            vehicle (dpd.driving.Vehicle): the vehicle to drive along the route
            buffer (float): a multiplier to control for timetable padding
        """
        self["time_to_next_stop"] = 0
        stops = self[self.stop_name != ""].index.values.tolist()
        stop = stops.pop(0)
        for next_stop in stops:
            speed_limits = list(self[stop:next_stop].speed_limit)[:-1]
            speed_limits.append(
                0.00001
            )  # if we have a speed_limit of 0, we get a division by zero error, but the vehicle should be going close to 0 at the stop.
            lengths = list(self[stop:next_stop].distance_to_next_point)[:-1]
            lengths.append(0.00001)
            self.at[stop, "time_to_next_stop"] = (
                vehicle.drive_between_stops(speed_limits, lengths)["time"].sum() - 1
            )  # subtract 1 to cancel out adding the extra speed limit and length
            stop = next_stop

    def folium_map(self, map=None):
        """
        A shortcut to create a folium map of the route.

        Args:
            map (folium.Map): an existing map to add the route to
        
        Returns:
            map (folium.Map): the map with the route on it
        """
        if not map:
            map = folium.Map(
                location=[
                    self["geometry"].to_crs(epsg="4326")[0].xy[1][0],
                    self["geometry"].to_crs(epsg="4326")[0].xy[0][0],
                ]
            )
        map.add_children(
            folium.features.GeoJson(self["geometry"].to_crs(epsg="4326").to_json())
        )
        return map
