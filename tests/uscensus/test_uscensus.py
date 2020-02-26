import unittest

from dpd.uscensus import get_geometry_for_states


class TestUSCensus(unittest.TestCase):
    def test_uscensus(self):
        self.assertIsNotNone(get_geometry_for_states("2016", ["11"]))


if __name__ == "__main__":
    unittest.main()
