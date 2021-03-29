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

DEFAULT_SPEED = 25 * units.imperial.mile / units.hour
DEFAULT_SPEED_UNIT = units.imperial.mile / units.hour


class OSMMap(Map):
    def __init__(self, region):
        super().__init__()
        self.region = region
        fp = get_data(region)
        self.osm = OSM(fp)
        self.osm.keep_node_info = True
        self.network = self.osm.get_network(
            "all",
            extra_attributes=[
                "lanes:forward",
                "lanes:backward",
                "cycleway:left",
                "cycleway:right",
            ],
        )
        self.node_tags = (
            self.create_node_tags_lookup()
        )  # Used to find traffic signals, all-way stops
        intersections = self.build_intersections()
        self.intersections = gpd.GeoDataFrame.from_dict(intersections, orient="index")
        self.intersections.crs = "EPSG:4326"
        roads = self.build_roads()
        self.roads = gpd.GeoDataFrame.from_dict(roads, orient="index")
        self.roads.crs = "EPSG:4326"
        logging.info(
            "Generated %s intersections and %s roads."
            % (len(self.intersections), len(self.roads))
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
        if speed == None:
            return DEFAULT_SPEED
        speed_split = speed.split()
        if len(speed_split) == 2:
            if speed_split[1] == "mph":
                speed_unit = units.imperial.mile / units.hour
            elif speed_split[1] == "km/h":
                speed_unit = units.kilometer / units.hour
            else:
                speed_unit = DEFAULT_SPEED_UNIT
            return speed_split[0] * speed_unit
        else:
            logging.warning("No speed unit: %s" % (speed,))
            return speed_split[0] * DEFAULT_SPEED_UNIT

    def create_road_segment(self, nodes, road_id):
        linestring = []
        for node in nodes:
            coordinates = self.osm._node_coordinates[node]
            linestring.append(Point(coordinates["lon"], coordinates["lat"]))
        road_geometry = LineString(linestring)
        if nodes[0] in self.intersections.index:
            start_node = self.intersections.loc[nodes[0]]["Intersection"]
        else:
            start_node = None
        if nodes[-1] in self.intersections.index:
            end_node = self.intersections.loc[nodes[-1]]["Intersection"]
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

    def lane_calculator(self, road):
        if road["oneway"] == "yes":
            if road["lanes:forward"]:
                number_of_lanes_forward = int(road["lanes:forward"])
            elif road["lanes"]:
                number_of_lanes_forward = int(road["lanes"])
            else:
                number_of_lanes_forward = 1
            number_of_lanes_backward = 0
        elif road["lanes:forward"]:
            number_of_lanes_forward = int(road["lanes:forward"])
            if road["lanes:backward"]:
                number_of_lanes_backward = int(road["lanes:backward"])
                if road["lanes"]:
                    if number_of_lanes_forward + number_of_lanes_backward != int(
                        road["lanes"]
                    ):
                        logging.warning(
                            "lanes:forward + lanes:backward != lanes %s" % road["name"]
                        )
            elif road["lanes"]:
                number_of_lanes_backward = int(road["lanes"]) - number_of_lanes_forward
            else:
                number_of_lanes_backward = 1
        elif road["lanes"]:
            if road["lanes"] == "1":
                logging.warning("two way road with only one lane %s" % road["id"])
                number_of_lanes_forward = 1
                number_of_lanes_backward = 1
            number_of_lanes_forward = math.ceil(int(road["lanes"]) / 2)
            number_of_lanes_backward = int(road["lanes"]) // 2
        else:
            number_of_lanes_forward = 1
            number_of_lanes_backward = 1
        return number_of_lanes_forward, number_of_lanes_backward

    def cycleway_calculator(self, road):
        cycleway_types = ["lane", "track"]
        if road["oneway"] == "yes":
            if road["cycleway"] in cycleway_types:
                cycleway_forward = road["cycleway"]
                cycleway_backward = None
            elif road["cycleway:right"] in cycleway_types:
                cycleway_forward = road["cycleway:right"]
                cycleway_backward = None
            elif road["cycleway:left"] in cycleway_types:
                cycleway_forward = road["cycleway:left"]
                cycleway_backward = None
        else:
            if road["cycleway"] in cycleway_types:
                cycleway_forward = road["cycleway"]
                cycleway_backward = road["cycleway"]
            elif road["cycleway:right"] in cycleway_types:
                cycleway_forward = road["cycleway:right"]
                if road["cycleway:left"] in cycleway_types:
                    cycleway_backward = road["cycleway:left"]
            elif road["cycleway:left"] in cycleway_types:
                cycleway_backward = road["cycleway:left"]
                cycleway_forward = None
            else:
                cycleway_forward = None
                cycleway_backward = None
        return cycleway_forward, cycleway_backward

    def build_roads(self):
        logging.info("Building roads...")
        roads = {}
        for _, road in tqdm(self.network.iterrows(), total=len(self.network)):
            number_of_lanes_forward, number_of_lanes_backward = self.lane_calculator(
                road
            )
            road_segments = self.build_road_segments(road)
            cycleway_forward, cycleway_backard = self.cycleway_calculator(road)
            for segment in road_segments:
                road_id = str(road["id"]) + ":S" + str(segment["road_id"]) + ":D0"
                r = Road(
                    road_id,
                    segment["road_geometry"],
                    segment["start_node"],
                    segment["end_node"],
                    number_of_lanes_forward,
                    cycleway=cycleway_forward,
                    max_speed=road["maxspeed"],
                )
                roads[road_id] = {
                    "geometry": r.geometry,
                    "Road": r,
                }
                if number_of_lanes_backward or cycleway_backward:
                    reversed_segment_road_geometry = LineString(
                        segment["road_geometry"].coords[::-1]
                    )  # Flip it around for the other direction
                    road_id = str(road["id"]) + ":S" + str(segment["road_id"]) + ":D1"
                    r = Road(
                        road_id,
                        reversed_segment_road_geometry,
                        segment["end_node"],
                        segment["start_node"],
                        number_of_lanes_backward,
                        cycleway=cycleway_backward,
                        max_speed=road["maxspeed"],
                    )
                    roads[road_id] = {
                        "geometry": r.geometry,
                        "Road": r,
                    }
        return roads
