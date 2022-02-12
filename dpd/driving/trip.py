from .stop import Stop
from dpd.geometry import MovingDict
import matplotlib.pyplot as plt

class Trip(MovingDict):
    """
    A class to describe a person or vehicle going from place to place.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_stop(self, geometry, distance_from_previous_stop=0, name="", arrival_time=None, departure_time=None, **kwargs):
        if  arrival_time:
            self.data[arrival_time] = Stop(name=name, geometry=geometry, distance_from_previous_stop = distance_from_previous_stop, **kwargs)
        if departure_time:
            self.data[departure_time] = Stop(name=name, geometry=geometry, distance_from_previous_stop = distance_from_previous_stop, **kwargs)

    def plot_schedule(self, **kwargs):
        geodataframe = self.to_geodataframe(columns=["name", "geometry", "distance_from_previous_stop"])
        geodataframe["distance_from_previous_stop"].plot(**kwargs)
        for idx, row in geodataframe.iterrows():
            plt.annotate(
                text=row["name"],
                xy=(idx, row["distance_from_previous_stop"])
            )
