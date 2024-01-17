import logging

from geopandas import GeoDataFrame
from shapely.geometry import Point
from shapely.ops import linemerge
from tqdm import tqdm

from dpd.osm import OSM
from dpd.shapely import snap_point_to_linestring

from .route import Route


class Network:
    """
    a transporation network with one or more routes
    """

    def __init__(self, routes=None):
        if routes:
            self.routes = routes
        else:
            self.routes = {}

    def add_route(self, index, route):
        self.routes[index] = route

    def from_gtfs(feed, *args, **kwargs):
        network = Network()
        for route_id in feed.routes["route_id"]:
            logging.info("Adding route %s." % (route_id))
            network.add_route(
                route_id, Route.from_gtfs(feed, route_id, *args, **kwargs)
            )
        return network

    @staticmethod
    def from_felt_geojson(geodataframe, *args, **kwargs):
        network = Network()
        for line_index, line in geodataframe[
            geodataframe["felt-type"] == "Path"
        ].iterrows():
            linestring = linemerge(line.geometry)
            stops = []
            for stop_index, stop in geodataframe[
                (geodataframe["felt-color"] == line["felt-color"])
                & (geodataframe["felt-type"] == "Place")
            ].iterrows():
                linestring, new_stop = snap_point_to_linestring(
                    linestring, stop["geometry"]
                )
                stops.append({"felt-text": stop["felt-text"], "geometry": new_stop})
            geometry = [Point(x, y) for (x, y) in linestring.coords]
            route = GeoDataFrame(
                geometry, columns=["geometry"], crs="EPSG:4326"
            )
            route["name"] = None
            for stop in stops:
                stop_index = list(linestring.coords).index(stop["geometry"].coords[0])
                route.loc[stop_index, "name"] = stop["felt-text"]
            network.add_route(line["felt-color"], Route(route, *args, **kwargs))
        return network

    @staticmethod
    def from_osm_relations(relations, osm=OSM(), *args, **kwargs):
        network = Network()
        for relation in tqdm(relations):
            logging.info("Adding route %s." % (relation))
            osm.download_relation(relation)
            network.add_route(
                relation, Route.from_osm_relation(relation, *args, **kwargs)
            )
        return network

    @staticmethod
    def from_osm_query(query, osm=OSM(), *args, **kwargs):
        """
        Build a network from an OpenStreetMap Overpass API Query

        Example Query:
            [out:json][timeout:25];
            (
              relation["network"="Metro Rail"];

            );
            out body;
            >;
            out skel qt;
        """
        result = osm.execute_query(query)
        relations = []
        for element in result["elements"]:
            if element["type"] == "relation":
                if "→" in element["tags"]["name"] or "=>" in element["tags"]["name"]:
                    logging.info(
                        "Found route %s with id %s."
                        % (element["tags"]["name"], element["id"])
                    )
                    relations.append(element["id"])
        return Network.from_osm_relations(relations, *args, **kwargs)

    def plot_folium(self, *args, **kwargs):
        for route in tqdm(self.routes):
            self.routes[route].plot_folium(*args, **kwargs)
