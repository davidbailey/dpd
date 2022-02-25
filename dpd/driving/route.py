from datetime import timedelta, datetime

from astropy import units
from astropy.time import TimeDelta
import folium
from geopandas import GeoDataFrame
from numpy import sqrt
from pandas import concat, DataFrame
from pyproj import CRS
from shapely.geometry import LineString, MultiLineString, MultiPoint, Point
from shapely.ops import linemerge, nearest_points


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
        self.gague = gague * units.meter
        self.max_cant = max_cant * units.meter
        self.max_cant_deficiency = max_cant_deficiency * units.meter

    @property
    def stops(self):
        return self[self["name"].notnull()]

    @property
    def way(self):
        return LineString(self["geometry"])

    @property
    def distances(self):
        """
        Returns a list of distances between every pair of points along the route.
        The length of the list is one less than the number of points on the route.
        """
        self.to_crs("North America Albers Equal Area Conic", inplace=True)
        distances = []
        for i in range(len(self) - 1):
            distances.append(
                self.geometry.iloc[i].distance(self.geometry.iloc[i + 1]) * units.meter
            )
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
                * units.meter
            )
        return radius_of_curvature

    def speed_limit(self, radius_of_curvature):
        """
        from https://en.wikipedia.org/wiki/Minimum_railway_curve_radius
        """
        return sqrt(
            9.81
            * units.meter
            / (units.second * units.second)
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

    def drive(self, vehicle, dwell_time):
        self.to_crs("North America Albers Equal Area Conic", inplace=True)
        distances = self.distances
        speed_limits = self.speed_limits
        segments = [
            DataFrame.from_dict(
                {
                    "distance": [0, 0],
                    "time": [0, dwell_time],
                    "name": [self.stops.name.iloc[0], self.stops.name.iloc[0]],
                }
            ),
        ]
        for i in range(len(self.stops.index) - 1):
            segments.append(
                vehicle.drive_between_stops(
                    speed_limits[self.stops.index[i] : self.stops.index[i + 1]] + [0],
                    distances[self.stops.index[i] : self.stops.index[i + 1]] + [0],
                )
            )
            segments.append(
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
        return concat(segments, ignore_index=True)

    def _trip_geometry(self, row):
        if row.distance:
            return LineString(
                [
                    self.way.interpolate(row.total_distance.value),
                    self.way.interpolate((row.total_distance - row.distance).value),
                ]
            )
        else:
            return self.way.interpolate(
                0 if row.total_distance == 0 else row.total_distance.value
            )

    def trip(
        self, vehicle, dwell_time, start_time=datetime(1970, 1, 1), geometry=False
    ):
        trip = self.drive(vehicle, dwell_time)
        trip["total_time"] = trip.time.cumsum()
        trip["timedelta"] = trip.total_time.map(lambda x: TimeDelta(x).to_datetime())
        trip["datetime"] = trip.timedelta + start_time
        trip["total_distance"] = trip.distance.cumsum()
        trip.set_index("datetime", inplace=True)
        if geometry:
            trip["geometry"] = trip.apply(lambda row: self._trip_geometry(row), axis=1)
        return GeoDataFrame(trip, crs=self.crs)

    def add_stop(self, geometry, name):
        """
        Adds a stop at the given geometry named name.
        """
        if geometry in list(self.geometry):
            self.loc[self.geometry == geometry, "name"] = name
        else:
            self.loc[
                self.geometry == nearest_points(MultiPoint(self.geometry), geometry)[0],
                "name",
            ] = name

    def remove_stop(self, name):
        """
        Removes all stos named name.
        """
        self.loc[self.name == name, "name"] = None

    def from_way(way, crs, *args, **kwargs):
        route = []
        for i in range(len(way.coords)):
            route.append({"geometry": Point(way.coords[i][0], way.coords[i][1])})
        return Route(route, crs=crs, *args, **kwargs)

    def from_ways(ways, crs, *args, **kwargs):
        ways_merged = linemerge(ways)
        if (
            type(ways_merged) == MultiLineString
        ):  # there are multiple, disconnected ways: pick the longest one
            longest_length = 0
            for way in ways_merged:
                if way.length > longest_length:
                    longest_length = way.length
                    longest_way = way
            way = longest_way
        else:
            way = ways_merged
        return Route.from_way(way, crs=crs, *args, **kwargs)

    def from_gtfs(feed, route_id, service_id, shape_id=None, *args, **kwargs):
        trips = feed.trips[
            (feed.trips["route_id"] == route_id)
            & (feed.trips["service_id"] == service_id)
        ]["trip_id"]
        if not shape_id:
            shape_id = feed.trips[feed.trips["trip_id"] == trips.iloc[0]].shape_id.iloc[
                0
            ]
        line = feed.build_geometry_by_shape([shape_id])[shape_id]
        route = Route.from_way(line, crs=CRS.from_epsg(4326), *args, **kwargs)
        for stop_id in feed.stop_times[feed.stop_times["trip_id"] == trips.iloc[0]][
            "stop_id"
        ]:
            stop = feed.stops[feed.stops.stop_id == stop_id]
            route.add_stop(Point(stop.stop_lon, stop.stop_lat), stop.stop_name.iloc[0])
        return route

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
        route = Route.from_ways(ways, crs=CRS.from_epsg(4326), *args, **kwargs)
        for member in osm.relations[relation]["members"]:
            if member["type"] == "node":
                route.add_stop(
                    osm.nodes[member["ref"]].geo,
                    osm.nodes[member["ref"]].osm["tags"]["name"],
                )
        return route

    def plot_folium(self, folium_map):
        self.to_crs(CRS.from_epsg(4326))
        tooltip = folium.features.GeoJsonTooltip(fields=["name"])
        geojson = folium.GeoJson(
            self.stops[["name", "geometry"]].to_json(), tooltip=tooltip
        )
        geojson.add_to(folium_map)
        folium.PolyLine(
            list(zip(list(self.way.coords.xy[1]), list(self.way.coords.xy[0])))
        ).add_to(folium_map)
