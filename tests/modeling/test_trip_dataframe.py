import unittest

from dpd.modeling import TripDataFrame

ST = "ri"
YEAR = "2017"


class TestTripDataFrame(unittest.TestCase):
    def test_trip_dataframe(self):
        TripDataFrame.from_lodes(ST, YEAR)


if __name__ == "__main__":
    unittest.main()
