import unittest

from dpd.modeling import OriginDestinationDataFrame

ST = "ri"
YEAR = "2017"


class TestOriginDestinationDataFrame(unittest.TestCase):
    def test_origin_destination_dataframe(self):
        OriginDestinationDataFrame.from_lodes(ST, YEAR)


if __name__ == "__main__":
    unittest.main()
