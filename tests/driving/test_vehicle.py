import unittest

from dpd.driving import Vehicle

class TestVehicle(unittest.TestCase):
    def test_vehicle(self):
        self.vehicle = Vehicle(24.5872, 1.3, -1.3, name="max_speed_55_mph_vehicle")


if __name__ == "__main__":
    unittest.main()
