from datetime import timedelta, datetime

from geopandas import GeoDataFrame
from numpy import sqrt
from pandas import concat, DataFrame
from pyproj import CRS
from shapely.geometry import MultiLineString, Point
from shapely.ops import linemerge


from dpd.geometry import circle_from_three_circumference_points


class Route(GeoDataFrame):
    """
    the route a vehicle takes
    """

    def __init__(
        self,
        data,
        gague=1.435,
        max_cant=0.1524,
        max_cant_deficiency=0.075,
        *args,
        **kwargs
    ):
        super().__init__(data, *args, **kwargs)
        self.gague = gague
        self.max_cant = max_cant
        self.max_cant_deficiency = max_cant_deficiency

    @property
    def stops(self):
        return self[self["name"].notnull()]

    @property
    def distances(self):
        """
        Returns a list of distances between every pair of points along the route.
        The length of the list is one less than the number of points on the route.
        """
        self.to_crs("North America Albers Equal Area Conic", inplace=True)
        distances = []
        for i in range(len(self) - 1):
            distances.append(self.geometry.iloc[i].distance(self.geometry.iloc[i + 1]))
        return distances

    @property
    def radius_of_curvature(self):
        """
        Returns a list of the radii of curvature between every three points along the route.
        The lenght of the list is two less than the number of points on the route.
        """
        self.to_crs("North America Albers Equal Area Conic", inplace=True)
        radius_of_curvature = []
        for i in range(len(self) - 2):
            radius_of_curvature.append(
                circle_from_three_circumference_points(
                    (self.geometry.iloc[i].x, self.geometry.iloc[i].y),
                    (self.geometry.iloc[i + 1].x, self.geometry.iloc[i + 1].y),
                    (self.geometry.iloc[i + 2].x, self.geometry.iloc[i + 2].y),
                )[1]
            )
        return radius_of_curvature

    def speed_limit(self, radius_of_curvature):
        return sqrt(
            9.8
            * (self.max_cant + self.max_cant_deficiency)
            * radius_of_curvature
            / self.gague
        )

    @property
    def speed_limits(self, which_radius="both"):
        """
        Returns a list of maximum speeds between every pair of points along the route based on the radius of curvature.
        The length of the list is one less than the number of points on the route.
        """
        radius_of_curvature = self.radius_of_curvature
        speed_limits_mapped = list(map(self.speed_limit, radius_of_curvature))
        if which_radius == "first":
            return [None] + speed_limits_mapped
        elif which_radius == "last":
            return speed_limits_mapped + [None]
        elif which_radius == "both":
            speed_limits = [speed_limits_mapped[0]]
            for i in range(len(speed_limits_mapped) - 1):
                speed_limits.append(
                    min(speed_limits_mapped[i], speed_limits_mapped[i + 1])
                )
            speed_limits.append(speed_limits_mapped[-1])
            return speed_limits

    def drive(self, vehicle, dwell_time, start_time=datetime(1970, 1, 1)):
        self.to_crs("North America Albers Equal Area Conic", inplace=True)
        distances = self.distances
        speed_limits = self.speed_limits
        trip = [
            DataFrame.from_dict(
                {
                    "distance": [0, 0],
                    "time": [0, dwell_time],
                    "name": [self.stops.name.iloc[0], self.stops.name.iloc[0]],
                }
            ),
        ]
        for i in range(len(self.stops.index) - 1):
            trip.append(
                vehicle.drive_between_stops(
                    speed_limits[self.stops.index[i] : self.stops.index[i + 1] - 1]
                    + [0],
                    distances[self.stops.index[i] : self.stops.index[i + 1] - 1] + [0],
                )
            )
            trip.append(
                DataFrame.from_dict(
                    {
                        "distance": [0, 0],
                        "time": [0, dwell_time],
                        "name": [
                            self.stops.name[self.stops.index[i + 1]],
                            self.stops.name[self.stops.index[i + 1]],
                        ],
                    }
                )
            )
        trip = concat(trip, ignore_index=True)
        trip["total_time"] = trip.time.cumsum()
        trip["timedelta"] = trip.total_time.map(lambda x: timedelta(seconds=x))
        trip["datetime"] = trip.timedelta + start_time
        trip["total_distance"] = trip.distance.cumsum()
        trip.set_index("datetime", inplace=True)
        return trip

    def from_gtfs(gtfs, *args, **kwargs):
        pass

    def from_osm_relation(osm, relation, *args, **kwargs):
        """
        Build a route from OpenStreetMaps data
        Args:
            osm (dpd.OSM.osm): the osm that contains the route as a relation
            relation (int): the relation to build a route for
        Returns:
            dpd.driving.Route: a route to drive
        """
        route = []
        ways = [
            osm.ways[member["ref"]].geo
            for member in osm.relations[relation]["members"]
            if member["type"] == "way"
            and member["role"]
            not in [
                "stop_entry_only",
                "stop_exit_only",
                "platform_entry_only",
                "platform_exit_only",
                "stop",
                "platform",
            ]
        ]
        ways_merged = linemerge(ways)
        if (
            type(ways_merged) == MultiLineString
        ):  # the relation may contain multiple, disconnected ways: pick the longest one
            longest_length = 0
            for way in ways_merged:
                if way.length > longest_length:
                    longest_length = way.length
                    longest_way = way
            way = longest_way
        else:
            way = ways_merged
        for i in range(len(way.coords)):
            route.append({"geometry": Point(way.coords[i][0], way.coords[i][1])})
        for member in osm.relations[relation]["members"]:
            if member["type"] == "node":
                for item in route:
                    if item["geometry"] == osm.nodes[member["ref"]].geo:
                        item["name"] = osm.nodes[member["ref"]].osm["tags"]["name"]
        return Route(route, crs=CRS.from_epsg(4326), *args, **kwargs)
