from .criterion import Criterion


class AttributeCriterion(Criterion):
    """
    a Criterion that returns the .name attribute on the class
    """

    def __init__(self, name, lower=True, *args, **kwargs):
        attribute_name = name.replace(" ", "_")
        if lower:
            attribute_name = attribute_name.lower()
        super().__init__(
            name=name, function=lambda x: getattr(x, attribute_name), *args, **kwargs
        )
