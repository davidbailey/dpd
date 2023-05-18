from haversine import haversine_vector, Unit
from pandas import DataFrame


class DistanceDataFrame(DataFrame):
    """
    This is a class to compute an Origin-Destination DataFrame.
    It maps a distance, cost, or time function to origins and destinations. Output is a DataFrame with origins as rows and destinations as columns.
    The result can be merged with the origins or destinations dataframe. e.g. pandas.merge(origins, accessibility, left_index=True, right_index=True)
    
    * Index is Origins
    * Columns are Destinations
    * Value is distance from origin to destination (Meters, Kilometers, Seconds, Minutes, Dollars)
    * Often built from Zones as a square matrix, but origins and destinations can be the same or different
    """

    @staticmethod
    def from_origins_destinations(
        origins, destinations, method="distance", distance_unit=1, mode="walking", *args, **kwargs
    ):
        """
        origins (geopandas.GeoSeries): GeoSeries of list of origin points
        destinations (geopandas.GeoSeries): GeoSeries of list of destination points
        method
        distance_unit: unit to apply to all values. Currently only supported with method=distance
        method ["distance", "haversine", "OSRM"]: method used for calculating distance. Distance requires Points to be in meters. haversine and OSRM reqiures Points to be in (lon, lat).
        mode ["walking", "cycling", "driving"]: mode that is passed to OSRM.
        """
        if method=="distance":
            for name in [origins.crs.name, destinations.crs.name]:
                if "Albers_Equal_Area_Conic" not in name:
                    raise ValueError(
                        "CRS does not contain Albers_Equal_Area_Conic. Results will not be accurate"
                    )
            data = []
            for index in destinations.index:
                data.append(
                    origins.distance(destinations[index]).map(lambda x: x * distance_unit)
                )
            return DistanceDataFrame(
                data, index=destinations.index, columns=origins.index, *args, **kwargs
            ).T
        elif method=="haversine":
            return DistanceDataFrame(
                haversine_vector(
                    origins.map(lambda x: (x.y, x.x)).to_list(),
                    destinations.map(lambda x: (x.y, x.x)).to_list(),
                    Unit.METERS,
                    comb=True
                ),
                index=destinations.index,
                columns=origins.index,
                *args, **kwargs,
            )
        elif method="OSRM":
            pass
