import datetime
import logging


from astropy import units
import folium
import geopandas as gpd
from matplotlib import pyplot as plt
import movingpandas as mpd
import numpy as np
from pyproj import CRS
import requests
from shapely.geometry import box
from tqdm import tqdm


from dpd.modeling.agents.intersections.yield_intersection import YieldIntersection
from dpd.modeling.agents.people import Cyclist, Driver, Pedestrian
from dpd.mapping import Map, Lane, Sidewalk, Cycleway
from dpd.werkzeug import WerkzeugThread
from .people_flask_app import people_flask_app
from dpd.geometry import GeometricDict

SignalIntersection = YieldIntersection
StopIntersection = YieldIntersection


class ABTMMap(Map):
    def __init__(self, model, map_):
        self.model = model
        self.intersections = map_.intersections
        self.links = map_.links
        self.people = GeometricDict()
        self.transform_intersections_to_agent_based()
        self.transform_links_to_agent_based()
        self.clear_segments()

    def nodes_to_links(self, node_ids):
        """Takes a list of node_ids and a map and returns a list or links."""
        nodes = []
        # first we filter through all the nodes and find those that are actually intersections. for those that are not intersections, we assume they are part of the links. this may or may not be true.
        for node in node_ids:
            if node in self.intersections.keys():
                nodes.append(node)
        links = []
        for i in range(len(nodes) - 1):
            for link in self.intersections[nodes[i]].output_links:
                if (
                    link.output_intersection
                    and link.output_intersection.name == nodes[i + 1]
                ):
                    links.append(link)
                    break
        return links

    def add_person(self, person):
        """ maybe make People a Class and do this automatically """
        self.people[person.name] = person
        self.model.schedule.add(person)

    def transform_intersections_to_agent_based(self):
        for key, intersection in self.intersections.items():
            if hasattr(intersection, "type_"):
                intersection_type = intersection["type_"]
                if intersection_type == "Signal":
                    self.intersections[key] = SignalIntersection(
                        intersection, self.model
                    )
                elif intersection_type == "Stop":
                    self.intersections[key] = StopIntersection(intersection, self.model)
                else:
                    self.intersections[key] = YieldIntersection(
                        intersection, self.model
                    )
            else:
                self.intersections[key] = YieldIntersection(intersection, self.model)
            self.model.schedule.add(self.intersections[key])

    def transform_links_to_agent_based(self):
        """
        this must be run after transform_intersection_to_agent_based creates new Intersection objects.
        """
        for link in self.links.values():
            if link.input_intersection:
                link.input_intersection = self.intersections[
                    link.input_intersection.name
                ]
            if link.output_intersection:
                link.output_intersection = self.intersections[
                    link.output_intersection.name
                ]
            for segment in link.segments:
                if type(segment) in [Lane]:
                    segment.allowed_users = [Cyclist, Pedestrian, Driver]
                elif type(segment) in [Sidewalk, Cycleway]:
                    segment.allowed_users = [Cyclist, Pedestrian]

    def clear_segments(self):
        """
        adds occupants to all segments. can also be run later to clear segments of occupants from past model
        """
        for link in self.links.values():
            for segment in link.segments:
                if segment is not None:
                    segment.occupants = []

    def nodes_to_links(self, node_ids):
        """Takes a list of node_ids and a map and returns a list or links."""
        nodes = []
        # first we filter through all the nodes and find those that are actually intersections. for those that are not intersections, we assume they are part of the links. this may or may not be true.
        for node in node_ids:
            if node in self.intersections.keys():
                nodes.append(node)
        links = []
        for i in range(len(nodes) - 1):
            for link in self.intersections[nodes[i]].output_links:
                if (
                    link.output_intersection
                    and link.output_intersection.name == nodes[i + 1]
                ):
                    links.append(link)
                    break
        return links

    def create_people_from_od(self, od):
        for _, person in tqdm(od.iterrows(), total=len(od)):
            route = self.nodes_to_links(
                person.routes[0]["legs"][0]["annotation"]["nodes"]
            )
            # todo - add other modes
            driver = Driver(self.model, person.home_geometry, route)
            self.people[driver.name] = driver
            self.model.schedule.add(driver)
        self.people.crs = "EPSG:4326"

    def post_people(self, url):
        crs = self.people.crs
        self.people.to_crs("EPSG:4326")
        p = requests.post(url, data={"people": self.people.to_json()})
        self.people.to_crs(crs)

    def simulate(
        self,
        number_of_rounds=10,
        time=datetime.datetime(1970, 1, 1, 0, 0, 0),
        post_people=False,
    ):
        trajectories = []
        aea = CRS.from_string("North America Albers Equal Area Conic")
        self.intersections.to_crs(aea)
        self.links.to_crs(aea)
        self.people.to_crs(aea)
        if post_people:
            werkzeug_thread = WerkzeugThread(people_flask_app())
            werkzeug_thread.start()
        for round_number in range(number_of_rounds):
            logging.info("Simulating round %s" % (round_number,))
            for person in self.people.values():
                trajectories.append(
                    {
                        "time": time,
                        "geometry": person.geometry,
                        "name": person.name,
                    }
                )
            if post_people:
                self.post_people("http://localhost:9000/people")
            self.model.step()
            time = time + datetime.timedelta(seconds=1)
        if post_people:
            werkzeug_thread.stop()
        gpd_trajectories = gpd.GeoDataFrame(trajectories, crs=aea).set_index("time")
        mpd_trajectories = mpd.TrajectoryCollection(gpd_trajectories, "name")
        return mpd_trajectories

    def plot(
        self,
        include_intersections=False,
        include_links=False,
        include_people=True,
        filter_box=None,
        **kwargs,
    ):
        fig = plt.figure(figsize=(18, 16))
        ax = fig.add_subplot(111)
        if include_intersections:
            self.intersections.plot(filter_box, ax=ax, **kwargs)
        if include_links:
            self.intersections.plot(filter_box, ax=ax, **kwargs)
        if include_people:
            self.people.plot(filter_box, ax=ax, **kwargs)
        plt.show()

    def plot_folium(
        self,
        include_intersections=False,
        include_links=False,
        include_people=True,
        filter_box=None,
        **kwargs,
    ):
        folium_map = folium.Map(location=(38.9, -77), zoom_start=12)
        if include_links:
            self.links.plot_folium(
                folium_map=folium_map, filter_box=filter_box, **kwargs
            )
        if include_intersections:
            self.intersections.plot_folium(
                folium_map=folium_map, filter_box=filter_box, **kwargs
            )
        if include_people:
            self.people.plot_folium(
                folium_map=folium_map, filter_box=filter_box, **kwargs
            )
        return folium_map
