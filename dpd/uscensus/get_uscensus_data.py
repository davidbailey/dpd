"""
A function to get data from the US Census API
"""
import logging

import pandas
import geopandas
import requests
from pyproj import CRS


def get_uscensus_data(year, state, data=["NAME"], with_geometry=False):
    """Gets the specified data from the US Census API and returns it as a Pandas DataFrame.

    Args:
        year (str): the year to get the data from
        state (str): the name of the state to get the data for
	data ([str]): the data to gather from the API
        with_geometry (bool): if geometric data should be added to the result

    Returns:
        pandas.DataFrame: A dataframe containing the data. If with_geometry is true, this is a geopandas.DataFrame
    """
    url = (
        "https://api.census.gov/data/"
        + year
        + "/acs/acs5?get="
        + ",".join(data)
        + "&for=tract:*&in=state:"
        + state
    )
    logging.debug("url: " + url):
    request = requests.get(url)
    dataframe = pandas.DataFrame(
        request.json()[1:], columns=request.json()[0], dtype="int"
    )
    if with_geometry:
        geometry = geopandas.read_file(
            "https://www2.census.gov/geo/tiger/TIGER"
            + year
            + "/TRACT/tl_"
            + year
            + "_"
            + state
            + "_tract.zip"
        )
        geometry.crs = CRS.from_epsg(4326)

        dataframe = pandas.merge(
            dataframe,
            geometry,
            how="inner",
            left_on=["state", "county", "tract"],
            right_on=["STATEFP", "COUNTYFP", "TRACTCE"],
        )
    return dataframe
