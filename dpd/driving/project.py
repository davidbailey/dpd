from dpd.cba import CostBenefitAnalysis
from dpd.mca import MultipleCriteriaAnalysis


class Project:
    """
    a transporation project
    """

    def __init__():
        pass

    @property
    def costs(self):
        pass

    @property
    def benefits(self):
        pass

    @property
    def cost_benefit_analysis(self):
        cost_benefit_analysis = CostBenefitAnalysis(start_year, duration)
        for cost in self.costs:
            cost_benefit_analysis.add_cost(cost)
        for benefit in self.benefits:
            cost_benefit_analysis.benefit(benefit)
        return cost_benefit_analysis

    @property
    def multiple_criteria_analysis(self):
        multiple_criteria_analysis = MultipleCriteriaAnalysis()
        return multiple_criteria_analysis

    def plot_folium(folium_map):
        pass
