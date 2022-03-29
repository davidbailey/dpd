from .criterion import Criterion


class DurationCriterion(Criterion):
    """
    a Criterion derived from the Duration of an Activity
    """

    def __init__(self, name, *args, **kwargs):
        super().__init__(
            name=name, function=lambda x: getattr(x, name).duration, *args, **kwargs
        )
