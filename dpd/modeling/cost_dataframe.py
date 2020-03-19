import math

import pandas


def gravity_model_function(distance, beta):
    return math.exp(-beta * distance)


class CostDataFrame(pandas.DataFrame):
    """
    A class to store a cost matrix and methods to create a cost matrix.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_centroid_distance_dataframe(
        centroid_distance_dataframe, beta, *args, **kwargs
    ):
        """
        A method to create a gravity model cost matrix from a CentroidDistanceDataFrame
        """
        origin_list = []
        for origin in centroid_distance_dataframe.index:
            destination_list = []
            for destination in centroid_distance_dataframe.columns:
                destination_list.append(
                    gravity_model_function(
                        centroid_distance_dataframe.loc[origin][destination], beta
                    )
                )
            origin_list.append(destination_list)
        return CostDataFrame(
            origin_list,
            index=centroid_distance_dataframe.index,
            columns=centroid_distance_dataframe.columns,
            *args,
            **kwargs
        )
