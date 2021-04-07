from dpd.geopandas import GeoObjectDataFrame


class People(GeoObjectDataFrame):
    """
    A class to hold People.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
