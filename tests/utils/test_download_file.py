import unittest

from dpd.utils import download_file

URL = "https://www.google.com/humans.txt"
LOCAL_FILENAME = "humans.txt"

class TestDownloadFile(unittest.TestCase):
    def test_download_file(self):
        self.assertEqual(download_file(URL), LOCAL_FILENAME)


if __name__ == "__main__":
    unittest.main()
