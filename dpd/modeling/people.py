from datetime import datetime, timedelta

import geopandas
import movingpandas
import pandas
import requests

from .agent_based_dict import AgentBasedDict
from mesa.datacollection import DataCollector


class People(AgentBasedDict):
    """
    A class to hold People.
    """

    def __init__(self, crs=None, *args, **kwargs):
        super().__init__(crs=crs, *args, **kwargs)
        self.data_collector = DataCollector(agent_reporters={"geometry": "geometry"})

    def to_crs(self, crs):
        """"""
        raise NotImplementedError(
            "I'm not able to change the crs on People. Maybe create a GeoDataFrame and then change the crs."
        )

    def add_person(self, person):
        self[person.name] = person
        self.model.schedule.add(person)

    def post_people(self, url):
        people = self.to_geopandas()
        people.to_crs("EPSG:4326")
        p = requests.post(url, data={"people": people.to_json()})

    def get_agent_vars_geodataframe(
        self, start_time=datetime(1970, 1, 1, 0, 0, 0)
    ):
        gdf = geopandas.GeoDataFrame(self.data_collector.get_agent_vars_dataframe())
        gdf.crs = self.crs
        one_day = timedelta(1)
        seconds_index = pandas.date_range(start_time, start_time + one_day, freq="S")[
            0 : len(gdf)
        ]
        gdf.index = gdf.index.set_levels(seconds_index, level=0)
        return gdf

    def get_trajectories(self):
        gdf = self.get_agent_vars_geodataframe()
        gdf.reset_index(level="AgentID", inplace=True)
        return movingpandas.TrajectoryCollection(gdf, "AgentID")
