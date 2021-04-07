from dpd.geopandas import GeoObjectDataFrame


class Intersections(GeoObjectDataFrame):
    """
    A class to hold Intersections.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
