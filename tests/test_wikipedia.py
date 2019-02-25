import unittest

from dpd.wikipedia import get_wikipedia_table

class TestWikipedia(unittest.TestCase):
    def test_get_wikipedia_table(self):
        states = get_wikipedia_table('https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code', 0)
        states.index = states['Name']
        state = states['Numeric code']['California']
        self.assertEqual(state, '06')

if __name__ == '__main__':
    unittest.main()
