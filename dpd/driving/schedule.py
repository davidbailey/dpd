class Schedule(GeoDataFrame):
    """
    the schedule for a route
    """

    def __init__(
        self,
        data,
        *args,
        **kwargs
    ):
        super().__init__(data, *args, **kwargs)


    @property
    def capacity(self):
        return None

