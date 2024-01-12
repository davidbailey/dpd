from haversine import Unit, haversine_vector
from pandas import DataFrame

from dpd.osrm import table


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
        origins, destinations, method="distance", distance_unit=1, *args, **kwargs
    ):
        """
        origins (geopandas.GeoSeries): GeoSeries of list of origin points
        destinations (geopandas.GeoSeries): GeoSeries of list of destination points
        method
        distance_unit: unit to apply to all values. Currently only supported with method=distance
        method ["distance", "haversine", "OSRM"]: method used for calculating distance. Distance requires Points to be in meters. haversine and OSRM reqiures Points to be in (lon, lat).
        mode ["walking", "cycling", "driving"]: mode that is passed to OSRM.
        """
        if method == "distance":
            if origins.crs != destinations.crs:
                raise ValueError(
                    "CRS does not match between origins and destinations. Results will not be accurate"
                )
            if origins.crs is not None and destinations.crs is not None:
                for name in [origins.crs.name, destinations.crs.name]:
                    if "WGS 84" not in name:
                        raise ValueError(
                            "CRS does not contain WGS 84. Results will not be accurate"
                        )
            data = []
            for index in destinations.index:
                data.append(
                    origins.distance(destinations[index]).map(
                        lambda x: x * distance_unit
                    )
                )
            return DistanceDataFrame(
                data, index=destinations.index, columns=origins.index, *args, **kwargs
            ).T
        elif method == "haversine":
            return DistanceDataFrame(
                haversine_vector(
                    origins.map(lambda x: (x.y, x.x)).to_list(),
                    destinations.map(lambda x: (x.y, x.x)).to_list(),
                    Unit.METERS,
                    comb=True,
                ),
                index=destinations.index,
                columns=origins.index,
                *args,
                **kwargs,
            )
        elif method == "OSRM":
            source_coordinates = ";".join(
                map(lambda x: str(x.x) + "," + str(x.y), origins.to_list())
            )
            destination_coordinates = ";".join(
                map(lambda x: str(x.x) + "," + str(x.y), destinations.to_list())
            )
            source_index = ";".join(map(str, range(len(origins))))
            destinations_index = ";".join(
                map(str, range(len(origins), len(origins) + len(destinations)))
            )

            response = table(
                origins=source_coordinates + ";",
                destinations=destination_coordinates,
                options="?sources=%s&destinations=%s"
                % (source_index, destinations_index),
            )
            return response
