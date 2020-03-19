import unittest

from dpd.modeling import Zones

ST = "44"
YEAR = "2017"
BETA = 0.001


class TestZones(unittest.TestCase):
    def test_zones(self):
        zones = Zones.from_uscensus(ST, YEAR)
        zones["Attraction"] = zones["Production"]
        # od = zones.calculate_origin_destination_dataframe(beta=BETA) # TODO figure out why this is broken


if __name__ == "__main__":
    unittest.main()
