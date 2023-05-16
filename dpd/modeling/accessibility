from pandas import DataFrame


class Accessibility(DataFrame):
    """
    Maps a cost/time/distance function to origins and destinations. Output is a DataFrame with origins as rows and destinations as columns.
    Can be merged with origins or destinations dataframe. e.g. pandas.merge(origins, accessibility, left_index=True, right_index=True)
    """
    @staticmethod
    def from_origins_destinations(origins, destinations, distance_unit=1, *args, **kwargs):
        """
        
        Add methods for distance (default), haversine, OSRM (with modes)
        This replaces CentroidDistanceDataFrame
        """
        data = []
        for index in destinations.index:
            data.append(origins.distance(destinations[index]).map(lambda x: x * distance_unit))
        return Accessibility(data, index=destinations.index, columns=origins.index, *args, **kwargs).T
