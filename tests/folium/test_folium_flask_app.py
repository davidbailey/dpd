import unittest

import folium
import pandas

from dpd.folium import folium_flask_app


class TestFoliumFlaskApp(unittest.TestCase):
    def test_folium_flask_app(self):
        self.app = folium_flask_app()


if __name__ == "__main__":
    unittest.main()
