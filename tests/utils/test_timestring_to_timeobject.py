import datetime
import unittest

from dpd.utils import timestring_to_timeobject

TIMESTRING = "00:24:23"


class TestTimestringToTimeobject(unittest.TestCase):
    def test_timestring_to_timeobject(self):
        self.assertEqual(
            timestring_to_timeobject(TIMESTRING),
            datetime.datetime(1900, 1, 1, 0, 24, 23),
        )


if __name__ == "__main__":
    unittest.main()
