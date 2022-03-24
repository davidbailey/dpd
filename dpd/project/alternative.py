from dpd.analysis import CostBenefitAnalysis


class Alternative:
    """
    an alternative
    """

    def __init__(self, name, routes=None):
        self.name = name
        if routes:
            self.routes = routes
        else:
            self.routes = []

    def add_route(self, route):
        self.routes.append(route)

    def travel_time(self, origin, destination):
        """Calculate accessibility to the stop, in_vehicle_travel_time, and accessibility to the destination"""
        pass

    @property
    def costs(self):
        costs = []
        for route in self.routes:
            costs.append(route.cost)
        return costs

    @property
    def benefits(self):
        benefits = []
        for route in self.routes:
            benefits.append(route.benefits)
        return benefits

    def cost_benefit_analysis(self, start_year, duration):
        cost_benefit_analysis = CostBenefitAnalysis(start_year, duration)
        for cost in self.costs:
            cost_benefit_analysis.add_cost(cost)
        for benefit in self.benefits:
            cost_benefit_analysis.benefit(benefit)
        return cost_benefit_analysis

    def plot_folium(self, folium_map):
        for route in self.routes:
            route.plot_folium(folium_map)
