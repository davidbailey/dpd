from dpd.analysis import MultipleCriteriaAnalysis


class Project:
    """
    a transporation project
    """

    def __init__(self, alternatives=None, criteria=None):
        if alternatives:
            self.alternatives = alternatives
        else:
            self.alternatives = {}
        if criteria:
            self.criteria = criteria
        else:
            self.criteria = {}

    def add_alternative(self, alternative):
        self.alternatives[alternative.name] = alternative

    def add_criterion(self, criterion):
        self.criteria[criterion.name] = criterion

    @property
    def multiple_criteria_analysis(self):
        multiple_criteria_analysis = MultipleCriteriaAnalysis(
            self.criteria.keys(), self.alternatives.keys()
        )
        for alternative in self.alternatives:
            for criterion in self.criteria:
                multiple_criteria_analysis.mca[alternative][criterion] = self.criteria[
                    criterion
                ].function(self.alternatives[alternative])
        return multiple_criteria_analysis

    @property
    def alternatives_analysis(self):
        for alternative in self.alternatives:
            print(alternative)

    @property
    def environmental_impact_document(self):
        pass
