import unittest

import folium
import pandas

from dpd.folium import plot_stops


class TestPlotStops(unittest.TestCase):
    def test_plot_stops(self):
        self.stops = {
            "stop_lat": 38.6258,
            "stop_lon": -121.475,
            "stop_name": "Test Stop",
        }
        self.stops = pandas.DataFrame(self.stops, index=[0])
        self.m = folium.Map()
        plot_stops(self.m, self.stops, with_contour=True, mode="driving")


if __name__ == "__main__":
    unittest.main()
