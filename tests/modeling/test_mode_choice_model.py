import unittest

from dpd.modeling import ModeChoiceModel


class TestModeChoiceModel(unittest.TestCase):
    def test_mode_choice_model(self):
        self.model = ModeChoiceModel()


if __name__ == "__main__":
    unittest.main()
