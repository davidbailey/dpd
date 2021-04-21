import unittest

import geopandas as gpd
from shapely.geometry import Polygon, box

from dpd.geopandas import filter_geodataframe


class Test_filter_geodataframe(unittest.TestCase):
    def test_filter_geodataframe(self):
        polygon = Polygon(box(0,0,10,10))
        geodataframe = gpd.GeoDataFrame([polygon], columns=["geometry"])
        filter_box = [-10,-10,5,5]
        filtered_geodataframe = filter_geodataframe(geodataframe, filter_box)
        self.assertEqual((0.0, 0.0, 5.0, 5.0), filtered_geodataframe.geometry[0].bounds)


if __name__ == "__main__":
    unittest.main()
