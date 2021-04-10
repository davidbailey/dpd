import requests

from .agent_based_dict import AgentBasedDict 
from mesa.datacollection import DataCollector


class People(AgentBasedDict):
    """
    A class to hold People.
    """
    def __init__(self, crs=None, *args, **kwargs):
        super().__init__(crs=crs, *args, **kwargs)
        self.data_collector = DataCollector(agent_reporters={"name": "name", "geometry": "geometry"})

    def to_crs(self, crs):
        """"""
        raise NotImplementedError("I'm not able to change the crs on People. Maybe create a GeoDataFrame and then change the crs.")

    def post_people(self, url):
        people = self.to_geopandas()
        people.to_crs("EPSG:4326")
        p = requests.post(url, data={"people": people.to_json()})
