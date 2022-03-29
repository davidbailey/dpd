from pandas import DataFrame, Series, isna, period_range

from .timeline import Timeline


class Alternative(DataFrame):
    """
    A class to create an Alternative made up of Activities
    """

    _metadata = ["name"]

    def __init__(self, name, *args, **kwargs):
        super().__init__(columns=["Start", "End", "Cost", "Benefit"], *args, **kwargs)
        self.name = name
        """
        Args:
            name (str): the name of the Alternative
        Returns:
            alternative (dpd.analysis.Alternative): an Alternative
        """

    def add_activity(self, activity):
        """
        Args:
            activity (dpd.analysis.Activity): an Activity to include in the Alternative
        """
        self.loc[activity.name] = activity

    @property
    def benefit(self):
        """
        Returns:
            benefit: the sum of all Benefits
        """
        return self.Benefit.sum()

    @property
    def cost(self):
        """
        Returns:
            cost: the sum of all Costs
        """
        return self.Cost.sum()

    @property
    def benefit_cost_ratio(self):
        """
        Returns:
            benefit_cost_ratio (float): the Benefit-Cost Ratio
        """
        return self.benefit / self.cost

    @property
    def start(self):
        """
        Returns:
            start (datetime.datetime): the earliest start time
        """
        return self.Start.min()

    @property
    def end(self):
        """
        Returns:
            end (datetime.datetime): the latest end time
        """
        return self.End.max()

    @property
    def duration(self):
        """
        Returns:
            duration (datetime.timedelta): the total duration of the Alternative
        """
        return self.end - self.start

    @property
    def timeline(self):
        """
        Returns:
            timeline (dpd.analysis.timeline): the timeline for all the Activities in the Alternative
        """
        return Timeline(self)

    def period_range_pivot(self, discount_rate=0.0, freq="Y"):
        """
        Args:
            freq (str)

        Returns:
            period_range_pivot (pandas.DataFrame): a Cost Table or Benefit Table
        """
        data = []
        for cost_or_benefit in ["Cost", "Benefit"]:
            for index, row in self.iterrows():
                pr = period_range(start=row.Start, end=row.End, freq=freq)
                data.append(
                    Series(
                        index=pr,
                        data=[row[cost_or_benefit] / len(pr) for x in range(len(pr))],
                        name=(cost_or_benefit, index),
                    )
                )
        return DataFrame(data).T

    @staticmethod
    def _plot_na(x):
        if isna(x):
            return 0
        return x.value

    def cash_flow_diagram(self, ax, freq="Y"):
        """
        Args:
            ax: the axis for the plot
            freq (str)
        """
        period_range_pivot = self.period_range_pivot(freq=freq)
        period_range_pivot["Cost"].applymap(self._plot_na).applymap(lambda x: -x).plot(
            ax=ax, kind="bar", color="red"
        )
        period_range_pivot["Benefit"].applymap(self._plot_na).plot(
            ax=ax, kind="bar", color="green"
        )

"""
    def discount(self, discount_year, discount_rate):
        apply_discount1 = lambda discount_year, row: row.apply(
            partial(apply_discount2, discount_year, row.name)
        )
        apply_discount2 = lambda discount_year, current_year, value: value / (
            1 + discount_rate
        ) ** (current_year - discount_year)
        dataframe = self.to_dataframe()
        dataframe = dataframe.apply(partial(apply_discount1, discount_year), axis=1)
        dataframe.loc["Sum"] = dataframe.sum()
        return dataframe
"""
