import logging

from tqdm import tqdm

from dpd.osm import OSM
from .route import Route


class Network:
    """
    a transporation network with one or more routes
    """

    def __init__(self, routes={}):
        self.routes = routes

    def add_route(self, index, route):
        self.routes[index] = route

    def from_gtfs(feed):
        pass

    def from_osm_relations(relations, osm=OSM()):
        network = Network()
        for relation in tqdm(relations):
            logging.info("Adding route %s." % (relation))
            osm.download_relation(relation)
            network.add_route(relation, Route.from_osm_relation(relation, osm))
        return network

    def from_osm_query(query, osm=OSM()):
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
        return Network.from_osm_relations(relations, osm)

    def plot_folium(self, *args, **kwargs):
        for route in tqdm(self.routes):
            self.routes[route].plot_folium(*args, **kwargs)
