from collections import Counter
import logging
import math

from astropy import units
import geopandas as gpd
import numpy as np
from pyrosm import get_data, OSM
from shapely.geometry import Point, LineString
from tqdm import tqdm


from dpd.mapping import Intersection, Map, Road


class OSMMap(Map):
    def __init__(self, region):
        super().__init__()
        self.region = region
        fp = get_data(region)
        self.osm = OSM(fp)
        self.osm.keep_node_info = True
        self.network = self.osm.get_network(
            "driving"
        )  # TODO Add cycling and walking networks.
        self.node_tags = self.create_node_tags_lookup()  # Used to find traffic signals.
        intersections = self.build_intersections()
        self.intersections = gpd.GeoDataFrame.from_dict(intersections, orient="index")
        self.intersections.crs = "EPSG:4326"
        roads = self.build_roads()
        self.roads = gpd.GeoDataFrame.from_dict(roads, orient="index")
        self.roads.crs = "EPSG:4326"
        logging.info(
            "Generated",
            len(self.intersections),
            "intersections and",
            len(self.roads),
            "roads.",
        )

    def create_node_tags_lookup(self):
        ids = np.concatenate([group["id"] for group in self.osm._nodes])
        tags = np.concatenate([group["tags"] for group in self.osm._nodes])
        return {ids[i]: tags[i] for i in range(0, len(ids))}

    def build_intersections(self):
        # Find all intersections by going through all the ways in the network and counting how often a node is referenced. If it is referenced more than once, it is an intersection.
        counter = Counter()
        for nodes in self.network.nodes:
            for node in nodes:
                counter[node] += 1
        intersections_list = [key for key, count in counter.items() if count >= 2]
        logging.info("Building intersections...")
        intersections = {}
        for intersection in tqdm(intersections_list):
            name = intersection
            coordinates = self.osm._node_coordinates[intersection]
            geometry = Point(coordinates["lon"], coordinates["lat"])
            if (
                self.node_tags[intersection]
                and "highway" in self.node_tags[intersection]
                and self.node_tags[intersection]["highway"] == "traffic_signals"
            ):
                type_ = "Signal"
            elif (
                self.node_tags[intersection]
                and "highway" in self.node_tags[intersection]
                and self.node_tags[intersection]["highway"] == "stop"
            ):
                type_ = "All-way Stop"
            else:
                type_ = "Yield"
            intersections[intersection] = {
                "geometry": geometry,
                "Type": type_,
                "Intersection": Intersection(name, geometry),
            }
        return intersections

    @staticmethod
    def speed_converter(speed):
        default_speed = 25 * units.imperial.mile / units.hour
        if speed == None:
            return default_speed
        r = [int(s) for s in speed.split() if s.isdigit()]
        if len(r) > 0:
            return r[0] * units.imperial.mile / units.hour
        else:
            return default_speed * units.imperial.mile / units.hour

    def create_road_segment(self, nodes, road_id):
        linestring = []
        for node in nodes:
            coordinates = self.osm._node_coordinates[node]
            linestring.append(Point(coordinates["lon"], coordinates["lat"]))
        road_geometry = LineString(linestring)
        if nodes[0] in self.intersections.index:
            start_node = nodes[0]
        else:
            start_node = None
        if nodes[-1] in self.intersections.index:
            end_node = nodes[-1]
        else:
            end_node = None
        return {
            "road_geometry": road_geometry,
            "start_node": start_node,
            "end_node": end_node,
            "road_id": road_id,
        }

    def build_road_segments(self, road):
        road_segments = []
        road_id = 0
        nodes = [road.nodes[0]]
        for node in road.nodes[1:]:
            nodes.append(node)
            if node in self.intersections.index:
                road_segments.append(self.create_road_segment(nodes, road_id))
                road_id += 1
                nodes = [node]
        if len(nodes) > 1:
            road_segments.append(self.create_road_segment(nodes, road_id))
        return road_segments

    def build_roads(self):
        logging.info("Building roads...")
        roads = {}
        for _, road in tqdm(self.network.iterrows(), total=len(self.network)):
            road_segments = self.build_road_segments(road)
            length_sum = 0
            number_of_lanes = road["lanes"]
            if road["oneway"]:
                if not number_of_lanes:
                    number_of_lanes = 1
                else:
                    number_of_lanes = int(number_of_lanes)
                for segment in road_segments:
                    length_sum += segment["road_geometry"].length
                    road_id = str(road["id"]) + ":S" + str(segment["road_id"])
                    if segment["start_node"]:
                        start_intersection = self.intersections.loc[
                            segment["start_node"]
                        ]["Intersection"]
                    else:
                        start_intersection = None
                    if segment["end_node"]:
                        end_intersection = self.intersections.loc[segment["end_node"]][
                            "Intersection"
                        ]
                    else:
                        end_intersection = None
                    r = Road(
                        road_id,
                        segment["road_geometry"],
                        start_intersection,
                        end_intersection,
                        number_of_lanes,
                    )
                    roads[road_id] = {
                        "geometry": r.geometry,
                        "Road": r,
                        "maxspeed": self.speed_converter(road["maxspeed"]),
                        "lanes": number_of_lanes,
                    }
            else:
                if not number_of_lanes:
                    number_of_lanes = 2
                elif number_of_lanes == "1":
                    number_of_lanes = 2
                    logging.warning("Two-way street with only one lane:", road.name)
                else:
                    number_of_lanes = int(number_of_lanes)
                number_of_lanes = number_of_lanes / 2  # TODO add turning lanes
                for segment in road_segments:
                    length_sum += segment["road_geometry"].length
                    road_id = str(road["id"]) + ":S" + str(segment["road_id"]) + ":D0"
                    if segment["start_node"]:
                        start_intersection = self.intersections.loc[
                            segment["start_node"]
                        ]["Intersection"]
                    else:
                        start_intersection = None
                    if segment["end_node"]:
                        end_intersection = self.intersections.loc[segment["end_node"]][
                            "Intersection"
                        ]
                    else:
                        end_intersection = None
                    r = Road(
                        road_id,
                        segment["road_geometry"],
                        start_intersection,
                        end_intersection,
                        int(number_of_lanes),
                    )
                    roads[road_id] = {
                        "geometry": r.geometry,
                        "Road": r,
                        "maxspeed": self.speed_converter(road["maxspeed"]),
                        "lanes": number_of_lanes,
                    }
                    reversed_segment_road_geometry = LineString(
                        segment["road_geometry"].coords[::-1]
                    )  # Flip it around for the other direction
                    road_id = str(road["id"]) + ":S" + str(segment["road_id"]) + ":D1"
                    if segment["end_node"]:
                        start_intersection = self.intersections.loc[
                            segment["end_node"]
                        ]["Intersection"]
                    else:
                        start_intersection = None
                    if segment["start_node"]:
                        end_intersection = self.intersections.loc[
                            segment["start_node"]
                        ]["Intersection"]
                    else:
                        end_intersection = None
                    r = Road(
                        road_id,
                        segment["road_geometry"],
                        start_intersection,
                        end_intersection,
                        int(number_of_lanes),
                    )
                    roads[road_id] = {
                        "geometry": r.geometry,
                        "Road": r,
                        "maxspeed": self.speed_converter(road["maxspeed"]),
                        "lanes": number_of_lanes,
                    }
        return roads
