import unittest

from dpd.folium import folium_flask_app


class TestFoliumFlaskApp(unittest.TestCase):
    def test_folium_flask_app(self):
        folium_flask_app()


if __name__ == "__main__":
    unittest.main()
