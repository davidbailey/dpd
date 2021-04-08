import unittest

from shapely.geometry import Point
from pyproj import CRS
import folium

from dpd.geometry import GeometricDict


class GeometricClass:
    def __init__(self, geometry):
        self.geometry = geometry


class TestGeometricDict(unittest.TestCase):
    def test_geometric_dict(self):
        geometric_object = GeometricClass(Point(-77, 38.9))
        geometric_dict = GeometricDict()
        geometric_dict[123] = geometric_object
        geometric_dict[234] = geometric_object
        geometric_dict.to_geoseries()
        folium_map = folium.Map(location=(38.9, -77), zoom_start=12)
        geometric_dict.plot_folium(folium_map)
        crs_4326 = CRS.from_epsg(4326)
        aea = CRS.from_string("North America Albers Equal Area Conic")
        geometric_dict.crs = crs_4326
        geometric_dict.to_crs(aea)


if __name__ == "__main__":
    unittest.main()
