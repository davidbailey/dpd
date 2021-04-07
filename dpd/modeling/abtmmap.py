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

SignalIntersection = YieldIntersection
StopIntersection = YieldIntersection


class ABTMMap(Map):
    def __init__(self, model, map_):
        self.model = model
        self.intersections = map_.intersections
        self.links = map_.links
        self.people = gpd.GeoDataFrame(columns=["geometry", "Person"])
        self.intersections["object"] = self.intersections.apply(
            self.transform_intersection_to_agent_based,
            axis=1,
        )
        self.links.apply(self.transform_link_to_agent_based, axis=1)
        self.prepare_links()
        self.clear_segments()

    def prepare_links(self):
        for link in self.links["object"]:
            for segment in link.segments:
                if type(segment) in [Lane]:
                    segment.allowed_users = [Cyclist, Pedestrian, Driver]
                elif type(segment) in [Sidewalk, Cycleway]:
                    segment.allowed_users = [Cyclist, Pedestrian]

    def nodes_to_links(self, node_ids):
        """Takes a list of node_ids and a map and returns a list or links."""
        nodes = []
        # first we filter through all the nodes and find those that are actually intersections. for those that are not intersections, we assume they are part of the links. this may or may not be true.
        for node in node_ids:
            if node in self.intersections.index:
                nodes.append(node)
        links = []
        for i in range(len(nodes) - 1):
            for link in self.intersections.loc[nodes[i]]["object"].output_links:
                if (
                    link.output_intersection
                    and link.output_intersection.name == nodes[i + 1]
                ):
                    links.append(link)
                    break
        return links

    def add_person(self, person):
        self.people.loc[person.name] = [
            person.geometry,
            person,
        ]
        self.model.schedule.add(person)

    def transform_intersection_to_agent_based(self, intersection):
        if hasattr(intersection, "Type"):
            intersection_type = intersection["Type"]
            if intersection_type == "Signal":
                intersection = SignalIntersection(
                    intersection["object"], self.model
                )
            elif intersection_type == "Stop":
                intersection = StopIntersection(
                    intersection["object"], self.model
                )
            else:
                intersection = YieldIntersection(
                    intersection["object"], self.model
                )
        else:
            intersection = YieldIntersection(intersection["object"], self.model)
        self.model.schedule.add(intersection)
        return intersection

    def transform_link_to_agent_based(self, link):
        """
        this must be run after transform_intersection_to_agent_based creates new Intersection objects.
        """
        if link["object"].input_intersection:
            link["object"].input_intersection = self.intersections.loc[
                link["object"].input_intersection.name
            ]["object"]
        if link["object"].output_intersection:
            link["object"].output_intersection = self.intersections.loc[
                link["object"].output_intersection.name
            ]["object"]

    def clear_segments(self):
        """
        adds occupants to all segments. can also be run later to clear segments of occupants from past model
        """
        for link in self.links["object"]:
            for segment in link.segments:
                if segment is not None:
                    segment.occupants = []

    def nodes_to_links(self, node_ids):
        """Takes a list of node_ids and a map and returns a list or links."""
        nodes = []
        # first we filter through all the nodes and find those that are actually intersections. for those that are not intersections, we assume they are part of the links. this may or may not be true.
        for node in node_ids:
            if node in self.intersections.index:
                nodes.append(node)
        links = []
        for i in range(len(nodes) - 1):
            for link in self.intersections.loc[nodes[i]]["object"].output_links:
                if (
                    link.output_intersection
                    and link.output_intersection.name == nodes[i + 1]
                ):
                    links.append(link)
                    break
        return links

    def create_people_from_od(self, od):
        people = {}
        for _, person in tqdm(od.iterrows(), total=len(od)):
            route = self.nodes_to_links(
                person.routes[0]["legs"][0]["annotation"]["nodes"]
            )
            # todo - add other modes
            driver = Driver(self.model, person.home_geometry, route)
            people[driver.name] = {"geometry": driver.geometry, "Person": driver}
            self.model.schedule.add(driver)
        self.people = gpd.GeoDataFrame.from_dict(people, orient="index")
        self.people.crs = "EPSG:4326"

    def transform_people_to_aea(self):
        logging.info("Transforming people to AEA. This could take a while...")
        aea = CRS.from_string("North America Albers Equal Area Conic")
        self.people.to_crs(aea, inplace=True)
        for _, person in self.people.iterrows():
            person["Person"].geometry = person["geometry"]

    def transform_people_to_epsg4326(self):
        self.people.to_crs("EPSG:4326", inplace=True)
        for _, person in self.people.iterrows():
            person["Person"].geometry = person["geometry"]

    def post_people(self, url):
        self.refresh_people_geometries()
        crs = self.people.crs
        self.people.to_crs("EPSG:4326", inplace=True)
        p = requests.post(url, data={"people": self.people["geometry"].to_json()})
        self.people.to_crs(crs, inplace=True)

    def refresh_people_geometries(self):
        self.people["geometry"] = self.people["Person"].map(
            lambda person: person.geometry
        )

    def simulate(
        self,
        number_of_rounds=np.inf,
        time=datetime.datetime(1970, 1, 1, 0, 0, 0),
        post_people=False,
    ):
        trajectories = []
        if not self.intersections.crs == CRS.from_string(
            "North America Albers Equal Area Conic"
        ):
            self.transform_intersections_to_aea()
        if not self.links.crs == CRS.from_string(
            "North America Albers Equal Area Conic"
        ):
            self.transform_links_to_aea()
        if not self.people.crs == CRS.from_string(
            "North America Albers Equal Area Conic"
        ):
            self.transform_people_to_aea()
        if post_people:
            werkzeug_thread = WerkzeugThread(people_flask_app())
            werkzeug_thread.start()
        for round_number in range(number_of_rounds):
            logging.info("Simulating round %s" % (round_number,))
            for _, person in self.people.iterrows():
                trajectories.append(
                    {
                        "time": time,
                        "geometry": person["Person"].geometry,
                        "name": person.name,
                    }
                )
            if post_people:
                self.post_people("http://localhost:9000/people")
            self.model.step()
            time = time + datetime.timedelta(seconds=1)
        if post_people:
            werkzeug_thread.stop()
        gpd_trajectories = gpd.GeoDataFrame(trajectories).set_index("time")
        gpd_trajectories.crs = CRS.from_string("North America Albers Equal Area Conic")
        gpd_trajectories.to_crs("EPSG:4326", inplace=True)
        mpd_trajectories = mpd.TrajectoryCollection(gpd_trajectories, "name")
        return mpd_trajectories

    def plot(
        self,
        include_intersections=False,
        include_links=False,
        include_people=True,
        filter_box=None,
    ):
        fig = plt.figure(figsize=(18, 16))
        ax = fig.add_subplot(111)
        if filter_box:
            filter_df = GeoDataFrame(Polygon(box(filter_box)), columns=["geometry"])
            filter_df = "EPSG:4326"
        else:
            filter_df = None
        if include_intersections:
            self.plot_df(ax, self.intersections, filter_df)
        if include_links:
            self.plot_df(ax, self.links, filter_df)
        if include_people:
            self.plot_df(ax, self.people, filter_df)
        plt.show()

    def plot_folium(
        self,
        include_intersections=False,
        include_links=False,
        include_people=True,
        folium_map=None,
        filter_box=None,
    ):
        if not folium_map:
            folium_map = folium.Map(location=(38.9, -77), zoom_start=12)
        if filter_box:
            filter_df = GeoDataFrame(Polygon(box(filter_box)), columns=["geometry"])
            filter_df.crs = "EPSG:4326"
        else:
            filter_df = None
        if include_links:
            if not "number_of_segments" in self.links.columns:
                self.links["number_of_segments"] = self.links["object"].map(
                    lambda link: len(link.segments)
                )
            style_function = lambda x: {"weight": x["properties"]["number_of_segments"]}
            self.plot_folium_df(
                folium_map,
                self.links[["geometry", "number_of_segments"]],
                filter_df,
                style_function=style_function,
            )
        if include_intersections:
            if not "name" in self.intersections.columns:
                self.intersections["name"] = self.intersections["object"].map(
                    lambda intersection: intersection.name
                )
            tooltip = (folium.features.GeoJsonTooltip(fields=["name"]),)
            self.plot_folium_df(
                folium_map,
                self.intersections[["geometry", "name"]],
                filter_df,
                tooltip=tooltip,
            )

        if include_people:
            if not "name" in self.people.columns:
                self.people["name"] = self.people["Person"].map(
                    lambda person: person.name
                )
            self.plot_folium_df(
                folium_map,
                self.people[["geometry", "name"]],
                filter_df,
                tooltip=tooltip,
            )
        return folium_map
