import unittest

from shapely.geometry import LineString

from dpd.mapping import Link

URL = "https://streetmix.net/api/v1/streets/2df276b0-a26a-11eb-a7b4-a104f581a3c9"


class TestLink(unittest.TestCase):
    def test_link(self):
        link = Link(name="test", geometry=LineString([(0, 0), (1, 1)]))
        link.update_segments_from_streetmix(URL)


if __name__ == "__main__":
    unittest.main()
