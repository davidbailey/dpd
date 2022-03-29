from pandas import Series


class Activity(Series):
    """
    an activity: something to do
    """

    def __init__(self, name, start, end, cost, benefit, *args, **kwargs):
        """
        Args:
            name (str): a name for the Activity
            start (datetime.datetime): when the Activity starts
            end (datetime.datetime): when the Activity ends
            cost (astropy.units.Quantity): the cost to perform the Activity
            benefit (astropy.units.Quantity): the benefit gained from performing the Activity

        Returns:
            activity (dpd.analysis.Activity)
        """
        super().__init__(
            data={"Start": start, "End": end, "Cost": cost, "Benefit": benefit},
            name=name,
            *args,
            **kwargs
        )

    @property
    def duration(self):
        """
        Returns:
            duration (datetime.timedelta): the total duration of the Activity
        """
        return self.End - self.Start
