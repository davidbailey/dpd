import unittest

from dpd.osm import OSM

relation = 2351006
name = "E Line (Expo): 7th Street / Metro Center → Downtown Santa Monica"


class TestOSM(unittest.TestCase):
    def test_osm(self):
        self.osm = OSM()
        self.osm.download_relation(relation)
        self.assertEqual(self.osm.relations[relation]["tags"]["name"], name)


if __name__ == "__main__":
    unittest.main()
