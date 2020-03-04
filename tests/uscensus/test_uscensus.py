import unittest

from dpd.uscensus import get_uscensus_data

YEAR = "2016"
STATE = "11"


class TestUSCensus(unittest.TestCase):
    def test_uscensus(self):
        self.dataframe = get_uscensus_data(YEAR, STATE, with_geometry=True)
        self.assertEqual(
            self.dataframe[self.dataframe["GEOID"] == "11001010900"]["AWATER"].values[
                0
            ],
            2936613,
        )


if __name__ == "__main__":
    unittest.main()
