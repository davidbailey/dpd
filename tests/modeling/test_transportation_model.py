import unittest

from dpd.modeling import TransportationModel


class TestTransportationModel(unittest.TestCase):
    def test_transportation_model(self):
        self.model = TransportationModel()


if __name__ == "__main__":
    unittest.main()
