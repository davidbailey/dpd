import unittest

from dpd.analysis import CostBenefitAnalysis

discount_rate = 0.03
start_year = 2017
duration = 3  # years


class TestCostBenefitAnalysis(unittest.TestCase):
    def test_cost_benefit_analysis(self):
        cba = CostBenefitAnalysis(start_year=start_year, duration=duration)
        cba.add_cost(name="cost 1", value=10, start_year=start_year, duration=2)
        cba.add_cost(name="cost 2", value=10, start_year=start_year, duration=2)
        cba.add_benefit(
            name="benefit 1", value=20, start_year=start_year + 1, duration=2
        )
        cba.add_benefit(
            name="benefit 2", value=20, start_year=start_year + 1, duration=2
        )
        cba_table = cba.discount(start_year, discount_rate).T
        self.assertEqual(
            cba_table["Sum"]["Benefits Total"] / cba_table["Sum"]["Costs Total"],
            1.9417475728155342,
        )
        cba.cash_flow_diagram()


if __name__ == "__main__":
    unittest.main()
