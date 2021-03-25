import unittest

from dpd.geometry import dms_to_dd

DMS_DD = [
    ("40°48′31″N", 40.808611111111105),
    ("74°1′13.39″W", -74.02038611111111),
    ("34.0°N", 34.0),
    ("118.2°W", -118.2),
]


class TestDMStoDD(unittest.TestCase):
    def test_dms_to_dd(self):
        for dms, dd in DMS_DD:
            self.assertEqual(dms_to_dd(dms), dd)


if __name__ == "__main__":
    unittest.main()
