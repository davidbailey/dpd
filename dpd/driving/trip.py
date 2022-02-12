from dpd.geometry import MovingDict
import matplotlib.pyplot as plt

class Trip(MovingDict):
    """
    A class to describe a person or vehicle going from place to place.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_stop(self, geometry, distance, name="", arrival_time=None, departure_time=None, **kwargs):
        if  arrival_time:
            self.data[arrival_time] = {"geometry": geometry, "distance": distance, "name": name, **kwargs}
        if departure_time:
            self.data[departure_time] = {"geometry": geometry, "distance": distance, "name": name, **kwargs}

    def plot_schedule(self, **kwargs):
        geodataframe = self.to_dataframe(columns=["geometry", "distance"])
        geodataframe["distance"].plot(**kwargs)
        for idx, row in geodataframe.iterrows():
            plt.annotate(
                text=row["name"],
                xy=(idx, row["distance"])
            )
