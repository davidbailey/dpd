import pandas
import numpy

class MultipleCriteriaAnalysis:
    def __init__(self, attributes, alternatives, monte_carlo=False):
        self.attributes = attributes
        self.alternatives = alternatives
        self.monte_carlo = monte_carlo
        if monte_carlo:
            monte_carlo = ['Mean', 'Standard Deviation', 'Distribution']
            index = pandas.MultiIndex.from_product([attributes, monte_carlo])
            self.mca = pandas.DataFrame(numpy.zeros((len(attributes) * len(monte_carlo), len(alternatives))),
                                        index=index, columns=alternatives, dtype='object')
        else:
            self.mca = pandas.DataFrame(numpy.zeros((len(attributes), len(alternatives))),
                                        index=attributes, columns=alternatives)
        self.weights = pandas.Series(numpy.ones(len(attributes)), index=attributes)


    def to_d3(self):
        data = {"name": "Multiple Criteria Analysis", "children": []}
        for attribute in self.attributes:
            children = []
            for alternative in self.alternatives:
                if self.monte_carlo:
                    children.append({'name': alternative, 'mean': self.mca[alternative][attribute]['Mean'],
                                     'stddev': self.mca[alternative][attribute]['Standard Deviation'],
                                     'distribution': self.mca[alternative][attribute]['Distribution']})
                else:
                    children.append({'name': alternative, 'mean': self.mca[alternative][attribute]})
            data['children'].append({'name': attribute, 'weight': self.weights[attribute], 'alternatives': children})
        return data
