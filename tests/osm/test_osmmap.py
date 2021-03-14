import unittest

from dpd.osm import OSMMap

REGION = "District of Columbia"


class TestOSMMap(unittest.TestCase):
    def test_osmmap(self):
        self.osm = OSMMap(REGION)


if __name__ == "__main__":
    unittest.main()
