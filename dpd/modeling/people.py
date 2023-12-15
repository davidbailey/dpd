import logging
from datetime import datetime, timedelta

import geopandas
import movingpandas
import pandas
import requests
from mesa.datacollection import DataCollector
from pyproj import CRS
from tqdm import tqdm

from dpd.modeling.agents.people import Cyclist, Driver, Pedestrian
from dpd.werkzeug import WerkzeugThread

from .agent_based_dict import AgentBasedDict
from .agent_based_intersections import AgentBasedIntersections
from .agent_based_links import AgentBasedLinks
from .mode_choice_model import ModeChoiceModel
from .people_flask_app import people_flask_app


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
        """ """
        raise NotImplementedError(
            "I'm not able to change the crs on People. Maybe create a GeoDataFrame and then change the crs."
        )

    def add_person(self, person):
        self[person.name] = person
        self.model.schedule.add(person)

    def create_people_from_od(self, od):
        mode_choice_model = ModeChoiceModel()
        mode_choice_model.add_mode(Driver, 0.8)
        mode_choice_model.add_mode(Cyclist, 0.1)
        mode_choice_model.add_mode(Pedestrian, 0.1)
        for _, person in tqdm(od.iterrows(), total=len(od)):
            route = self.intersections.nodes_to_links(
                person.routes[0]["legs"][0]["annotation"]["nodes"]
            )
            mode = mode_choice_model.predict()
            person = mode(self.model, person.home_geometry, route)
            self.add_person(person)

    def post_people(self, url, timeout=60):
        people = self.to_geopandas()
        people.to_crs("EPSG:4326")
        return requests.post(url, data={"people": people.to_json()}, timeout=timeout)

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
                self.post_people(post_people_url)
        if post_people_url:
            werkzeug_thread.stop()
