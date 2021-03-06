"""
A module to create a multiple-criteria analysis
"""

import pandas
import numpy


class MultipleCriteriaAnalysis:
    """
    A module to create a multiple-criteria analysis
    """

    def __init__(self, attributes, alternatives, monte_carlo=False):
        self.attributes = attributes
        self.alternatives = alternatives
        self.monte_carlo = monte_carlo
        if monte_carlo:
            monte_carlo = ["Mean", "Standard Deviation", "Distribution"]
            index = pandas.MultiIndex.from_product([attributes, monte_carlo])
            self.mca = pandas.DataFrame(
                numpy.zeros((len(attributes) * len(monte_carlo), len(alternatives))),
                index=index,
                columns=alternatives,
                dtype="object",
            )
        else:
            self.mca = pandas.DataFrame(
                numpy.zeros((len(attributes), len(alternatives))),
                index=attributes,
                columns=alternatives,
            )
        self.weights = pandas.Series(numpy.ones(len(attributes)), index=attributes)

    def from_csvs(
        self, mca_file="mca.csv", weights_file="weights.csv", monte_carlo=False
    ):
        mca = MultipleCriteriaAnalysis([], [])
        if monte_carlo:
            mca.mca = pandas.read_csv(mca_file, index_col=[0, 1])
            mca.mca.index.names = [None] * len(mca.mca.index.names)
            mca.attributes = list(mca.mca.index[0])
            mca.monte_carlo = True
        else:
            mca.mca = pandas.read_csv(mca_file)
            mca.attributes = list(mca.mca.index)
            mca.monte_carlo = False
        mca.alternatives = list(mca.mca.columns)
        mca.weights = pandas.read_csv(weights_file)
        return mca

    def to_csvs(self, mca_file="mca.csv", weights_file="weights.csv"):
        self.mca.to_csv(mca_file)
        self.weights.to_csv(weights_file)

    def compute(self):
        return self.weights.T.dot(
            self.mca.div(self.mca.sum(axis=1), axis=0)
        ).sort_values(ascending=False)

    def to_d3(self):
        normalized_mca = self.mca.div(self.mca.sum(axis=1), axis=0)
        normalized_mca_with_inverse = normalized_mca.apply(
            lambda x: (1 - x) / (len(self.alternatives) - 1)
            if self.weights[x.name] < 0
            else x,
            axis=1,
        )
        data = {"name": "Multiple Criteria Analysis", "children": []}
        for attribute in self.attributes:
            children = []
            for alternative in self.alternatives:
                if self.monte_carlo:
                    children.append(
                        {
                            "name": alternative,
                            "mean": normalized_mca_with_inverse[alternative][attribute][
                                "Mean"
                            ],
                            "stddev": normalized_mca_with_inverse[alternative][
                                attribute
                            ]["Standard Deviation"],
                            "distribution": normalized_mca_with_inverse[alternative][
                                attribute
                            ]["Distribution"],
                        }
                    )
                else:
                    children.append(
                        {
                            "name": alternative,
                            "mean": normalized_mca_with_inverse[alternative][attribute],
                        }
                    )
            data["children"].append(
                {
                    "name": attribute,
                    "weight": self.weights[attribute],
                    "alternatives": children,
                }
            )
        return data

    def to_d3_radar_chart(self):
        normalized_mca = self.mca.div(self.mca.sum(axis=1), axis=0)
        normalized_mca_with_inverse = normalized_mca.apply(
            lambda x: (1 - x) / (len(self.alternatives) - 1)
            if self.weights[x.name] < 0
            else x,
            axis=1,
        )
        legend_options = self.alternatives
        d = []
        for alternative in self.alternatives:
            alternative_d = []
            for attribute in self.attributes:
                alternative_d.append(
                    {
                        "axis": attribute,
                        "value": normalized_mca_with_inverse[alternative][attribute],
                    }
                )
            d.append(alternative_d)
        return (legend_options, d, "Alternative")
