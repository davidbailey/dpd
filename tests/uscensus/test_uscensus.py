import unittest

from dpd.uscensus import get_geometry_for_states


class TestUSCensus(unittest.TestCase):
    def test_uscensus(self):
        self.geometry = get_geometry_for_states("2016", ["11"])
        self.assertEqual(
            self.geometry[geometry["GEOID"] == "11001010900"]["AWATER"], 2936613
        )


if __name__ == "__main__":
    unittest.main()
