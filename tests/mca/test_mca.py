import unittest

from dpd.mca import MultipleCriteriaAnalysis

attributes = ["Cost", "Time", "Comfort"]
alternatives = ["Tram", "Bus"]

class TestMCA(unittest.TestCase):
    def test_mca(self):
        self.mca = MultipleCriteriaAnalysis(attributes, alternatives)
        self.mca.mca["Tram"]["Cost"] = 200
        self.mca.mca["Bus"]["Cost"] = 100
        self.mca.mca["Tram"]["Time"] = 50
        self.mca.mca["Bus"]["Time"] = 100
        self.mca.mca["Tram"]["Comfort"] = 800
        self.mca.mca["Bus"]["Comfort"] = 500
        self.assertEqual(self.mca.mca.to_csv(), ',Tram,Bus\nCost,200.0,100.0\nTime,50.0,100.0\nComfort,800.0,500.0\n')
        legend_options, d, title = self.mca.to_d3_radar_chart()
        self.assertEqual(legend_options, ['Tram', 'Bus'])
        self.assertEqual(d, [[{'axis': 'Cost', 'value': 0.6666666666666666}, {'axis': 'Time', 'value': 0.3333333333333333}, {'axis': 'Comfort', 'value': 0.6153846153846154}], [{'axis': 'Cost', 'value': 0.3333333333333333}, {'axis': 'Time', 'value': 0.6666666666666666}, {'axis': 'Comfort', 'value': 0.38461538461538464}]])
        self.assertEqual(title, 'Alternative')


if __name__ == "__main__":
    unittest.main()
