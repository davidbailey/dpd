class Stop:
    """
    A class to describe a stop along a Trip.
    """

    def __init__(self, name, geometry, **kwargs):
        self.name = name
        self.geometry = geometry
        self.__dict__.update(kwargs)
