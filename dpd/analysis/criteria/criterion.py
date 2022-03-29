class Criterion:
    """
    A criterion is a tool used for a multiple-criteria analysis to compare different alternatives. It consists of a name and a value which is returned by a function.
    """

    def __init__(self, name, function, weight=1):
        self.name = name
        self.function = function
        self.weight = weight

    def compute(self, x):
        self.function(x) * self.weight
