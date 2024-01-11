import folium
from astropy import units
from astropy.constants import g0
from geopandas import GeoDataFrame
from numpy import concatenate, minimum, sqrt
from pyproj import CRS
from shapely.geometry import LineString, MultiLineString, MultiPoint, Point
from shapely.ops import linemerge, nearest_points

from dpd.geometry import GeometricDict, circle_from_three_points
from dpd.osm import OSM

from .stop import Stop


class Route(GeoDataFrame):
    """
    the route a vehicle takes
    """

    _metadata = ["gague", "max_cant", "max_cant_deficiency"]

    def __init__(
        self,
        data,
        gague=1.435 * units.meter,
        max_cant=0.1524 * units.meter,
        max_cant_deficiency=0.075 * units.meter,
        *args,
        **kwargs
    ):
        super().__init__(data, *args, **kwargs)
        self.gague = gague
        self.max_cant = max_cant
        self.max_cant_deficiency = max_cant_deficiency

    @property
    def reversed(self):
        route_reversed = Route(self.iloc[::-1])
        route_reversed.index = range(len(route_reversed))
        return route_reversed

    @property
    def stops(self):
        return self[(self["name"] != "nan") & self.name.notnull()]

    @property
    def stops_dict(self):
        stops_dict = GeometricDict(crs=self.crs)
        for stop in self.stops.index:
            stops_dict[self.loc[stop]["name"]] = Stop(self.loc[stop]["geometry"])
        return stops_dict

    @property
    def way(self):
        return LineString(self["geometry"])

    @property
    def distances(self):
        """
        Returns a list of distances between every pair of points along the route.
        The length of the list is one less than the number of points on the route.
        """
        self.to_crs(epsg=4087, inplace=True)
        distances = []
        for i in range(len(self) - 1):
            distances.append(self.geometry.iloc[i].distance(self.geometry.iloc[i + 1]))
        return distances * units.meter

    @property
    def radius_of_curvature(self):
        """
        Returns a list of the radii of curvature between every three points along the route.
        The lenght of the list is two less than the number of points on the route.
        """
        self.to_crs(epsg=4087, inplace=True)
        radius_of_curvature = []
        for i in range(len(self) - 2):
            radius_of_curvature.append(
                circle_from_three_points(
                    (self.geometry.iloc[i].x, self.geometry.iloc[i].y),
                    (self.geometry.iloc[i + 1].x, self.geometry.iloc[i + 1].y),
                    (self.geometry.iloc[i + 2].x, self.geometry.iloc[i + 2].y),
                )[1]
            )
        return radius_of_curvature * units.meter

    def speed_limit(self, radius_of_curvature):
        """
        from https://en.wikipedia.org/wiki/Minimum_railway_curve_radius
        """
        return sqrt(
            g0
            * (self.max_cant + self.max_cant_deficiency)
            * radius_of_curvature
            / self.gague
        )

    @property
    def speed_limits(self):
        """
        Returns a list of maximum speeds between every pair of points along the route based on the radius of curvature.
        The length of the list is one less than the number of points on the route.
        """
        A = self.speed_limit(self.radius_of_curvature)
        return concatenate(([A[0]], minimum(A[:-1], A[1:]), [A[-1]]))

    def _drive_geometry(self, row):
        if row.distance:
            return LineString(
                [
                    self.way.interpolate(row.total_distance.value),
                    self.way.interpolate((row.total_distance - row.distance).value),
                ]
            )
        else:
            return self.way.interpolate(row.total_distance.value)

    def segments(self, dwell_time):
        segments = []
        stops = self.stops
        distances = self.distances
        speed_limits = self.speed_limits
        segments.append(
            {"stop_name": stops["name"][stops.index[0]], "dwell_time": dwell_time}
        )
        for i in range(len(stops.index) - 1):
            segments.append(
                {
                    "distances": distances[stops.index[i] : stops.index[i + 1]],
                    "speed_limits": speed_limits[stops.index[i] : stops.index[i + 1]],
                }
            )
            segments.append(
                {
                    "stop_name": stops["name"][stops.index[i + 1]],
                    "dwell_time": dwell_time,
                }
            )
        return segments

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

    @staticmethod
    def from_way(way, crs, *args, **kwargs):
        route = []
        for i in range(len(way.coords)):
            route.append({"geometry": Point(way.coords[i][0], way.coords[i][1])})
        return Route(route, crs=crs, *args, **kwargs)

    @staticmethod
    def from_ways(ways, crs, *args, **kwargs):
        """
        If there are multiple, disconnected ways, pick the longest one.
        Note: this does a lenght calculation on an unknown crs. This may be inaccurate.
        """
        ways_merged = linemerge(ways)
        if isinstance(ways_merged, MultiLineString):
            longest_length = 0
            for way in ways_merged.geoms:
                if way.length > longest_length:
                    longest_length = way.length
                    longest_way = way
            way = longest_way
        else:
            way = ways_merged
        return Route.from_way(way, crs=crs, *args, **kwargs)

    @staticmethod
    def from_gtfs(feed, route_id, service_id=None, shape_id=None, *args, **kwargs):
        if service_id:
            trips = feed.trips[
                (feed.trips["route_id"] == route_id)
                & (feed.trips["service_id"] == service_id)
            ]["trip_id"]
        else:
            trips = feed.trips[feed.trips["route_id"] == route_id]["trip_id"]
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

    @staticmethod
    def from_osm_relation(relation, osm=None, *args, **kwargs):
        """
        Build a route from OpenStreetMaps data
        Args:
            relation (int): the relation to build a route for
            osm (dpd.OSM.osm): the osm that contains the route as a relation
        Returns:
            dpd.driving.Route: a route to drive
        """
        if osm is None:
            osm = OSM()
        osm.download_relation(relation)
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

    def plot_accessibility_contourf(self, folium_map, times, mode):
        self.to_crs(epsg=4087, inplace=True)
        stops_dict = self.stops_dict
        for stop in stops_dict:
            features = stops_dict[stop].accessibility_contourf_features(
                times, mode, crs=self.crs
            )
            features.to_crs(CRS.from_epsg(4326), inplace=True)
            folium.GeoJson(data=features).add_to(folium_map)

    def plot_accessibility_radius(self, folium_map, times, mode):
        self.to_crs(epsg=4087, inplace=True)
        stops_dict = self.stops_dict
        for stop in stops_dict:
            features = stops_dict[stop].accessibility_radius_features(
                times, mode, crs=self.crs
            )
            features.to_crs(CRS.from_epsg(4326), inplace=True)
            folium.GeoJson(data=features).add_to(folium_map)

    def plot_folium(
        self,
        folium_map,
        include_stops=True,
        include_accessibility_contourf=False,
        include_accessibility_radius=True,
        include_way=True,
        times=[5, 10, 15] * units.minute,
        mode="walking",
    ):
        if include_accessibility_contourf:
            self.plot_accessibility_contourf(folium_map, times=times, mode=mode)
        if include_accessibility_radius:
            self.plot_accessibility_radius(folium_map, times=times, mode=mode)
        self.to_crs(CRS.from_epsg(4326), inplace=True)
        if include_stops:
            tooltip = folium.features.GeoJsonTooltip(fields=["name"])
            geojson = folium.GeoJson(
                self.stops[["name", "geometry"]].to_json(), tooltip=tooltip
            )
            geojson.add_to(folium_map)
        if include_way:
            folium.PolyLine(
                list(zip(list(self.way.coords.xy[1]), list(self.way.coords.xy[0])))
            ).add_to(folium_map)
