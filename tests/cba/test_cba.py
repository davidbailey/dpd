import unittest

from dpd.cba import CostBenefitAnalysis

discount_rate = 0.03
start_year = 2017
duration = 3  # years


class TestCBA(unittest.TestCase):
    def test_cba(self):
        self.cba = CostBenefitAnalysis(start_year=start_year, duration=duration)
        self.cba.add_cost(name="cost 1", value=10, start_year=start_year, duration=2)
        self.cba.add_cost(name="cost 2", value=10, start_year=start_year, duration=2)
        self.cba.add_benefit(
            name="benefit 1", value=20, start_year=start_year + 1, duration=2
        )
        self.cba.add_benefit(
            name="benefit 2", value=20, start_year=start_year + 1, duration=2
        )
        self.cba_table = self.cba.discount(start_year, discount_rate).T
        self.assertEqual(
            self.cba_table["Sum"]["Benefits Total"]
            / self.cba_table["Sum"]["Costs Total"],
            1.9417475728155342,
        )


if __name__ == "__main__":
    unittest.main()
