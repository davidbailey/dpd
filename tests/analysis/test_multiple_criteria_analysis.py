import unittest

from dpd.analysis import MultipleCriteriaAnalysis

attributes = ["Cost", "Time", "Comfort"]
alternatives = ["Tram", "Bus"]


class TestMultipleCriteriaAnalysis(unittest.TestCase):
    def test_multiple_criteria_analysis(self):
        multiple_criteria_analysis = MultipleCriteriaAnalysis(attributes, alternatives)
        multiple_criteria_analysis.mca["Tram"]["Cost"] = 200
        multiple_criteria_analysis.mca["Bus"]["Cost"] = 100
        multiple_criteria_analysis.mca["Tram"]["Time"] = 50
        multiple_criteria_analysis.mca["Bus"]["Time"] = 100
        multiple_criteria_analysis.mca["Tram"]["Comfort"] = 800
        multiple_criteria_analysis.mca["Bus"]["Comfort"] = 500
        self.assertEqual(
            multiple_criteria_analysis.mca.to_csv(),
            ",Tram,Bus\nCost,200.0,100.0\nTime,50.0,100.0\nComfort,800.0,500.0\n",
        )
        legend_options, d, title = multiple_criteria_analysis.to_d3_radar_chart()
        self.assertEqual(legend_options, ["Tram", "Bus"])
        self.assertEqual(
            d,
            [
                [
                    {"axis": "Cost", "value": 0.6666666666666666},
                    {"axis": "Time", "value": 0.3333333333333333},
                    {"axis": "Comfort", "value": 0.6153846153846154},
                ],
                [
                    {"axis": "Cost", "value": 0.3333333333333333},
                    {"axis": "Time", "value": 0.6666666666666666},
                    {"axis": "Comfort", "value": 0.38461538461538464},
                ],
            ],
        )
        self.assertEqual(title, "Alternative")
        multiple_criteria_analysis.to_d3()
        multiple_criteria_analysis.to_csvs()
        multiple_criteria_analysis.from_csvs()


if __name__ == "__main__":
    unittest.main()
