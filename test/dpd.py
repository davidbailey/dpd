import unittest
import dpd
import pandas
import folium

class TestUSCensus(unittest.TestCase):
    def test_get_uscensus_population_by_tract():
        self.assertEqual(True, True)
    def test_get_uscensus_geometry():
        self.assertEqual(True, True)
    def add_density_to_tracts():
        self.assertEqual(True, True)
    def test_get_uscensus_density_by_tract():
        self.assertEqual(True, True)


class TestWikipedia(unittest.TestCase):
    def test_get_wikipedia_table(self):
        states = dpd.get_wikipedia_table('https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code', 0)
        states.index = states['Name']
        state = states['Numeric code']['California']
        self.assertEqual(state, '06')


class TestGTFS(unittest.TestCase):
    def test_url2gtfs():
        self.assertEqual(True, True)
    def test_get_rail_stops():
        self.assertEqual(True, True)
    def test_plot_stops():
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
