from dpd.analysis import MultipleCriteriaAnalysis


class Project:
    """
    a transporation project
    """

    def __init__(self, alternatives=[]):
        self.alternatives = alternatives

    def add_alternative(self, alternative):
        self.alternatives.append(alternative)

    @property
    def multiple_criteria_analysis(self):
        multiple_criteria_analysis = MultipleCriteriaAnalysis()
        return multiple_criteria_analysis

    @property
    def alternatives_analysis(self):
        pass

    @property
    def environmental_impact_document(self):
        pass
