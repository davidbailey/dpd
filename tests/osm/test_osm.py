import unittest

from dpd.osm import OSM

RELATION = 2351006
NAME = "Metro E Line: 7th Street/Metro Center → Downtown Santa Monica"


class TestOSM(unittest.TestCase):
    def test_osm(self):
        self.osm = OSM()
        self.osm.download_relation(RELATION)
        self.assertEqual(self.osm.relations[RELATION]["tags"]["name"], NAME)


if __name__ == "__main__":
    unittest.main()
