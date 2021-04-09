import folium

from dpd.geometry import GeometricDict


class People(GeometricDict):
    """
    A class to hold People.
    """

    def to_crs(self, crs):
        """"""
        raise NotImplementedError("I'm not able to change the crs on People")
