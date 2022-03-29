from .criterion import Criterion


class CostCriterion(Criterion):
    """
    a Criterion derived from the Cost of an Activity
    """

    def __init__(self, name, *args, **kwargs):
        """
        Args:
            name (str): the name of the Activity to get Cost values for. E.g. `Construction` will get values from alternative.Construction.Cost

        Returns:
            benefit_criterion (dpd.analysis.CostCriterion)
        """

        super().__init__(
            name=name, function=lambda x: getattr(x, name).cost, *args, **kwargs
        )
