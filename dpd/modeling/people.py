from datetime import datetime, timedelta
import logging

import geopandas
import movingpandas
import pandas
import requests
from mesa.datacollection import DataCollector
from tqdm import tqdm
from pyproj import CRS

from dpd.modeling.agents.people import Driver
from dpd.werkzeug import WerkzeugThread
from .people_flask_app import people_flask_app
from .agent_based_dict import AgentBasedDict
from .agent_based_intersections import AgentBasedIntersections
from .agent_based_links import AgentBasedLinks


class People(AgentBasedDict):
    """
    A class to hold People.
    """

    def __init__(self, map_, crs=None, *args, **kwargs):
        super().__init__(crs=crs, *args, **kwargs)
        self.intersections = AgentBasedIntersections(map_.intersections)
        self.links = AgentBasedLinks(map_.links)
        self.links.update_intersections(self.intersections)

        self.data_collector = DataCollector(agent_reporters={"geometry": "geometry"})

    def to_crs(self, crs):
        """"""
        raise NotImplementedError(
            "I'm not able to change the crs on People. Maybe create a GeoDataFrame and then change the crs."
        )

    def add_person(self, person):
        self[person.name] = person
        self.model.schedule.add(person)

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
            driver = Driver(self.model, person.home_geometry, route)
            self.add_person(driver)

    def post_people(self, url):
        people = self.to_geopandas()
        people.to_crs("EPSG:4326")
        return requests.post(url, data={"people": people.to_json()})

    def get_agent_vars_geodataframe(self, start_time=datetime(1970, 1, 1, 0, 0, 0)):
        gdf = geopandas.GeoDataFrame(self.data_collector.get_agent_vars_dataframe())
        gdf.crs = self.crs
        one_day = timedelta(1)
        index = pandas.date_range(start_time, start_time + one_day, freq="S")[
            0 : len(gdf)
        ]
        gdf.index = gdf.index.set_levels(index, level=0)
        return gdf

    def get_trajectories(self):
        gdf = self.get_agent_vars_geodataframe()
        gdf.reset_index(level="AgentID", inplace=True)
        return movingpandas.TrajectoryCollection(gdf, "AgentID")

    def simulate(
        self,
        number_of_rounds=10,
        post_people_url=None,
    ):
        aea = CRS.from_string("North America Albers Equal Area Conic")
        self.intersections.to_crs(aea)
        self.links.to_crs(aea)
        self.crs = self.links.crs
        self.data_collector.collect(self.model)
        if post_people_url:
            werkzeug_thread = WerkzeugThread(people_flask_app())
            werkzeug_thread.start()
            self.people.post_people(post_people_url)
        for round_number in range(number_of_rounds):
            logging.info("Simulating round %s" % (round_number,))
            self.model.step()
            self.intersections.model.step()
            self.data_collector.collect(self.model)
            if post_people_url:
                self.people.post_people(post_people_url)
        if post_people_url:
            werkzeug_thread.stop()
