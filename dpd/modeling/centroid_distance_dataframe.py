from shapely.geometry import Point
import pandas

from dpd.utils import epsg4326_to_aea


class CentroidDistanceDataFrame(pandas.DataFrame):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_centroids(centroids):
        """"""
        origin_list = []
        for origin_point in centroids:
            destination_list = []
            for destination_point in centroids:
                destination_list.append(origin_point.distance(destination_point))
            origin_list.append(destination_list)
        return CentroidDistanceDataFrame(
            origin_list, index=centroids.index, columns=centroids.index
        )
