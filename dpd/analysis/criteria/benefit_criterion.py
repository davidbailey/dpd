from .criterion import Criterion


class BenefitCriterion(Criterion):
    """
    a Criterion derived from the Benefit of an Activity
    """

    def __init__(self, name, *args, **kwargs):
        """
        Args:
            name (str): the name of the Activity to get Benefit values for. E.g. `Construction` will get values from alternative.Construction.Benefit

        Returns:
            benefit_criterion (dpd.analysis.BenefitCriterion)
        """
        super().__init__(
            name=name, function=lambda x: getattr(x, name).Benefit, *args, **kwargs
        )
