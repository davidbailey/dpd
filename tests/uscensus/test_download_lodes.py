import unittest

from dpd.uscensus import download_lodes_od, download_lodes_xwalk

YEAR = "2017"
ST = "ri"
TYPE_ = "JT00"
PART = "main"

class TestDownloadLODES(unittest.TestCase):
    def test_download_lodes(self):
        download_lodes_od(ST, PART, TYPE_, YEAR)
        download_lodes_xwalk(ST)


if __name__ == "__main__":
    unittest.main()
