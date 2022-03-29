from matplotlib.dates import date2num
from pandas import DataFrame


class Timeline(DataFrame):
    """
    a timeline
    """

    def __init__(self, *args, **kwargs):
        super().__init__(columns=["Start", "End"], *args, **kwargs)

    def add_activity(self, activity):
        self.loc[activity.name] = {"Start": activity.Start, "End": activity.End}

    def plot_gantt(self, ax):
        start = self.Start.map(date2num)
        end = self.End.map(date2num)
        ax.barh(self.index[::-1], end[::-1] - start[::-1], left=start[::-1])
        ax.xaxis_date()
        ax.grid(axis="x", alpha=0.5)
