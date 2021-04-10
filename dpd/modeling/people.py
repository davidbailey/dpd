import requests

from dpd.geometry import GeometricDict


class People(GeometricDict):
    """
    A class to hold People.
    """

    def to_crs(self, crs):
        """"""
        raise NotImplementedError("I'm not able to change the crs on People")

    def post_people(self, url):
        people = self.to_geopandas()
        people.to_crs("EPSG:4326")
        p = requests.post(url, data={"people": people.to_json()})
