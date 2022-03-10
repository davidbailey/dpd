"""
A class to query the Overpass API
"""
from collections import namedtuple
from time import sleep

import requests
from shapely.geometry import Point, LineString

OSMObject = namedtuple("OSMObject", "osm, geo")


class OSM:
    """
    A class to query the Overpass API
    """

    def __init__(self):
        self.url = "http://overpass-api.de/api/interpreter"
        self.nodes = {}
        self.ways = {}
        self.relations = {}

    def execute_query(self, query, retry_attempts=4):
        r = requests.get(self.url, params={"data": query})
        if not "application/json" in r.headers.get("Content-Type"):
            if retry_attempts:
                # sometimes we run into a rate limit so let's back off a bit
                print("Response is not JSON. Retrying. Response: %s" % (r))
                sleep(1)
                return self.execute_query(query, retry_attempts - 1)
            else:
                raise ValueError("Response is not JSON. Response: %s" % (r))
        return r.json()

    def add_node(self, osm):
        geo = Point(osm["lon"], osm["lat"])
        osm_object = OSMObject(osm, geo)
        self.nodes[osm["id"]] = osm_object
        return osm_object

    def download_node(self, node_id):
        query = "[out:json]; node(%s); out;" % (node_id)
        osm = self.execute_query(query)["elements"][0]
        return self.add_node(osm)

    def add_way(self, osm):
        geo = LineString(self.nodes[node].geo for node in osm["nodes"])
        osm_object = OSMObject(osm, geo)
        self.ways[osm["id"]] = osm_object
        return osm_object

    def download_way(self, way_id):
        query = "[out:json]; way(%s); >; out;" % (way_id)
        for element in self.execute_query(query)["elements"]:
            self.add_node(element)
        query = "[out:json]; way(%s); out;" % (way_id)
        osm = self.execute_query(query)["elements"][0]
        return self.add_way(osm)

    def add_relation(self, osm):
        self.relations[osm["id"]] = osm
        return osm

    def download_relation(self, relation_id):
        query = "[out:json]; relation(%s); >; out;" % (relation_id)
        for element in self.execute_query(query)["elements"]:
            if element["type"] == "node":
                self.add_node(element)
            elif element["type"] == "way":
                self.add_way(element)
        query = "[out:json]; relation(%s); out;" % (relation_id)
        response = self.execute_query(query)
        if not response["elements"]:
            raise ValueError("Elements is empty. Response: %s" % (response))
        osm = response["elements"][0]
        return self.add_relation(osm)
