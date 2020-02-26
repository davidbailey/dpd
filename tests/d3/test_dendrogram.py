import unittest

from dpd.d3 import dendrogram


class TestDendrogram(unittest.TestCase):
    def test_dendrogram(self):
        self.assertIsNotNone(dendrogram(["test"]))


if __name__ == "__main__":
    unittest.main()
