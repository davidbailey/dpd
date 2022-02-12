from dpd.geometry import MovingDict

class Trip(MovingDict):
    """
    A class to describe a person or vehicle going from place to place.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_stop(geometry, arrival_time=None, departure_time=None, **kwargs):
        if  arrival_time:
            self.data[arrival_time] = {"geometry": geometry, **kwargs}
        if departure_time:
            self.data[departure_time] = {"geometry": geometry, **kwargs}
