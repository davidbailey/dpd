import pandas
import numpy
from functools import partial

class CostBenefitAnalysis:
    def __init__(self, start_year, duration):
        self.start_year = start_year
        self.duration = duration
        self.costs = pandas.DataFrame(index=range(start_year, start_year + duration))
        self.benefits = pandas.DataFrame(index=range(start_year, start_year + duration))


    def add_cost_or_benefit(self, costs_or_benefits, name, value, start_year, duration):
        if start_year < self.start_year or start_year + duration > self.start_year + self.duration:
            raise ValueError('start_year and duration fall outside start_year and duration for cba')
        if name in costs_or_benefits.columns:
            raise ValueError('name already exists')
        cost_or_benefit = pandas.Series(numpy.zeros(self.duration), index=range(self.start_year, self.start_year + self.duration))
        for year in range(start_year, start_year + duration):
            cost_or_benefit[year] = value
        costs_or_benefits[name] = cost_or_benefit


    def add_benefit(self, name, value, start_year, duration):
        self.add_cost_or_benefit(self.benefits, name, value, start_year, duration)


    def add_cost(self, name, value, start_year, duration):
        self.add_cost_or_benefit(self.costs, name, value, start_year, duration)

 
    def to_dataframe(self):
        costs = self.costs
        costs['Costs Total'] = costs.T.sum()
        benefits = self.benefits
        benefits['Benefits Total'] = benefits.T.sum()
        df = pandas.concat([costs, benefits], axis=1)
        df['Benefits - Costs Total'] = benefits['Benefits Total'] - costs['Costs Total']
        return df


    def discount(self, discount_year, discount_rate):
        apply_discount1 = lambda discount_year, row: row.apply(partial(apply_discount2, discount_year, row.name))
        apply_discount2 = lambda discount_year, current_year, value: value / (1 + discount_rate) ** (current_year - discount_year)
        df = self.to_dataframe()
        df = df.apply(partial(apply_discount1, discount_year), axis=1)
        df.loc['Sum'] = df.sum()
        return df
