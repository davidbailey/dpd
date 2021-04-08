from collections import Counter
import logging
import math

from astropy import units
import numpy as np
from pyrosm import get_data, OSM
from shapely.geometry import Point, LineString
from tqdm import tqdm


from dpd.mapping import Intersection, Map, Link, Links
from dpd.geometry import GeometricDict

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
        self.intersections = GeometricDict(crs="EPSG:4326")
        self.build_intersections(self.intersections)
        self.links = GeometricDict(crs="EPSG:4326")
        self.build_links(self.links)
        logging.info(
            "Generated %s intersections and %s links."
            % (len(self.intersections), len(self.links))
        )

    def create_node_tags_lookup(self):
        ids = np.concatenate([group["id"] for group in self.osm._nodes])
        tags = np.concatenate([group["tags"] for group in self.osm._nodes])
        return {ids[i]: tags[i] for i in range(0, len(ids))}

    def build_intersections(self, intersections):
        # Find all intersections by going through all the ways in the network and counting how often a node is referenced. If it is referenced more than once, it is an intersection.
        counter = Counter()
        for nodes in self.network.nodes:
            for node in nodes:
                counter[node] += 1
        intersections_list = [key for key, count in counter.items() if count >= 2]
        logging.info("Building intersections...")
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
            intersections[intersection] = Intersection(name, geometry)
            intersections[intersection].type = (type_,)

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

    def create_link_segment(self, nodes, link_id):
        linestring = []
        for node in nodes:
            coordinates = self.osm._node_coordinates[node]
            linestring.append(Point(coordinates["lon"], coordinates["lat"]))
        link_geometry = LineString(linestring)
        if nodes[0] in self.intersections.keys():
            start_node = self.intersections[nodes[0]]
        else:
            start_node = None
        if nodes[-1] in self.intersections.keys():
            end_node = self.intersections[nodes[-1]]
        else:
            end_node = None
        return {
            "link_geometry": link_geometry,
            "start_node": start_node,
            "end_node": end_node,
            "link_id": link_id,
        }

    def build_link_segments(self, link):
        link_segments = []
        link_id = 0
        nodes = [link.nodes[0]]
        for node in link.nodes[1:]:
            nodes.append(node)
            if node in self.intersections.keys():
                link_segments.append(self.create_link_segment(nodes, link_id))
                link_id += 1
                nodes = [node]
        if len(nodes) > 1:
            link_segments.append(self.create_link_segment(nodes, link_id))
        return link_segments

    def lane_calculator(self, link):
        if link["oneway"] == "yes":
            if link["lanes:forward"]:
                number_of_lanes_forward = int(link["lanes:forward"])
            elif link["lanes"]:
                number_of_lanes_forward = int(link["lanes"])
            else:
                number_of_lanes_forward = 1
            number_of_lanes_backward = 0
        elif link["lanes:forward"]:
            number_of_lanes_forward = int(link["lanes:forward"])
            if link["lanes:backward"]:
                number_of_lanes_backward = int(link["lanes:backward"])
                if link["lanes"]:
                    if number_of_lanes_forward + number_of_lanes_backward != int(
                        link["lanes"]
                    ):
                        logging.warning(
                            "lanes:forward + lanes:backward != lanes %s" % link["name"]
                        )
            elif link["lanes"]:
                number_of_lanes_backward = int(link["lanes"]) - number_of_lanes_forward
            else:
                number_of_lanes_backward = 1
        elif link["lanes"]:
            if link["lanes"] == "1":
                logging.warning("two way link with only one lane %s" % link["id"])
                number_of_lanes_forward = 1
                number_of_lanes_backward = 1
            number_of_lanes_forward = math.ceil(int(link["lanes"]) / 2)
            number_of_lanes_backward = int(link["lanes"]) // 2
        else:
            number_of_lanes_forward = 1
            number_of_lanes_backward = 1
        return number_of_lanes_forward, number_of_lanes_backward

    def cycleway_calculator(self, link):
        cycleway_types = ["lane", "track"]
        if link["oneway"] == "yes":
            if link["cycleway"] in cycleway_types:
                cycleway_forward = link["cycleway"]
                cycleway_backward = None
            elif link["cycleway:right"] in cycleway_types:
                cycleway_forward = link["cycleway:right"]
                cycleway_backward = None
            elif link["cycleway:left"] in cycleway_types:
                cycleway_forward = link["cycleway:left"]
                cycleway_backward = None
            else:
                cycleway_forward = None
                cycleway_backward = None
        else:
            if link["cycleway"] in cycleway_types:
                cycleway_forward = link["cycleway"]
                cycleway_backward = link["cycleway"]
            elif link["cycleway:right"] in cycleway_types:
                cycleway_forward = link["cycleway:right"]
                if link["cycleway:left"] in cycleway_types:
                    cycleway_backward = link["cycleway:left"]
                else:
                    cycleway_backward = None
            elif link["cycleway:left"] in cycleway_types:
                cycleway_backward = link["cycleway:left"]
                cycleway_forward = None
            else:
                cycleway_forward = None
                cycleway_backward = None
        return cycleway_forward, cycleway_backward

    def build_links(self, links):
        logging.info("Building links...")
        for _, link in tqdm(self.network.iterrows(), total=len(self.network)):
            number_of_lanes_forward, number_of_lanes_backward = self.lane_calculator(
                link
            )
            link_segments = self.build_link_segments(link)
            cycleway_forward, cycleway_backward = self.cycleway_calculator(link)
            for segment in link_segments:
                link_id = str(link["id"]) + ":S" + str(segment["link_id"]) + ":D0"
                links[link_id] = Link(
                    link_id,
                    segment["link_geometry"],
                    segment["start_node"],
                    segment["end_node"],
                    number_of_lanes=number_of_lanes_forward,
                    cycleway=cycleway_forward,
                    max_speed=link["maxspeed"],
                )
                if number_of_lanes_backward or cycleway_backward:
                    reversed_segment_link_geometry = LineString(
                        segment["link_geometry"].coords[::-1]
                    )  # Flip it around for the other direction
                    link_id = str(link["id"]) + ":S" + str(segment["link_id"]) + ":D1"
                    links[link_id] = Link(
                        link_id,
                        reversed_segment_link_geometry,
                        segment["end_node"],
                        segment["start_node"],
                        number_of_lanes=number_of_lanes_backward,
                        cycleway=cycleway_backward,
                        max_speed=link["maxspeed"],
                    )
