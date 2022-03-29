from pandas import DataFrame, Series, to_numeric


class Decision(DataFrame):
    _metadata = ["criteria", "alternatives"]

    def __init__(self, criteria=None, alternatives=None, *args, **kwargs):
        if criteria:
            self.criteria = criteria
        else:
            self.criteria = {}
        if alternatives:
            self.alternatives = alternatives
        else:
            self.alternatives = {}
        data = []
        for alternative in self.alternatives:
            row = []
            for criterion in self.criteria:
                row.append(
                    self.criteria[criterion].function(self.alternatives[alternative])
                )
            data.append(row)
        super().__init__(
            data=data,
            index=self.alternatives.keys(),
            columns=self.criteria.keys(),
            *args,
            **kwargs
        )

    @property
    def weights(self):
        weights = {}
        for criterion in self.criteria:
            weights[criterion] = self.criteria[criterion].weight
        return Series(weights)

    @property
    def _weighted_decision(self):
        return (self * self.weights).apply(lambda x: x.astype(float))

    def add_criterion(self, criterion):
        self.criteria[criterion.name] = criterion
        data = []
        for alternative in self.alternatives:
            data.append(criterion.function(self.alternatives[alternative]))
        self[criterion.name] = data

    def add_alternative(self, alternative):
        self.alternatives[alternative.name] = alternative
        data = []
        for criterion in self.criteria:
            data.append(self.criteria[criterion].function(alternative))
        self.loc[alternative.name] = data

    def plot(self, *args, **kwargs):
        return self._weighted_decision.plot(*args, **kwargs)

    def multiple_criteria_decision_analysis(self, method="weighted_sum_model"):
        """
        https://en.wikipedia.org/wiki/Multiple-criteria_decision_analysis
        weighted_sum_model: https://en.wikipedia.org/wiki/Weighted_sum_model
        weighted_product_model: https://en.wikipedia.org/wiki/Weighted_product_model
        """
        if method == "weighted_sum_model":
            return self._weighted_decision.sum(axis=1)
        elif method == "weighted_product_model":
            pass
