import unittest

from dpd.wikipedia import get_wikipedia_table


class TestGetWikipediaTable(unittest.TestCase):
    def test_get_wikipedia_table(self):
        states = get_wikipedia_table(
            "https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code"
        )
        states.index = states["Name"]
        state = states["Numeric code"]["California"]
        self.assertEqual(state, "06")


if __name__ == "__main__":
    unittest.main()
