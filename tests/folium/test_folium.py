import unittest

import folium
import pandas

from dpd.folium import plot_stops


class TestFolium(unittest.TestCase):
    def test_folium(self):
        self.stops = {"stop_lat": 38.6258, "stop_lon": -121.475, "stop_name": "Test Stop"}
        self.stops = pandas.DataFrame(self.stops, index=[0])
        self.m = folium.Map()
        plot_stops(self.m, self.stops)


if __name__ == "__main__":
    unittest.main()
