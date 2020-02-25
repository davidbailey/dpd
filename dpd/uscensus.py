"""
A set of functions to get data from the US Census API
"""
import pandas
import geopandas
import requests

def get_uscensus_data_by_tract(year, state, county, data):
    url = 'https://api.census.gov/data/' + year + '/acs/acs5?get=NAME'
    for datum in data.values():
        url += ',' + datum
    url += '&for=tract:*&in=state:' + state + '&in=county:' + county
    request = requests.get(url)
    tracts = pandas.DataFrame(
        request.json()[1:],
        columns=['NAME'] + list(data.keys()) + ['state', 'county', 'tract'],
        dtype='int'
    )
    return tracts


def get_uscensus_data_for_states(year, states, data):
    return pandas.concat(
        [
            get_uscensus_data_by_tract(
                year=year,
                state=state,
                county="*",
                data=data,
            )
            for state in states
        ]
    )


def get_geometry_for_states(year, states):
    geometry = pandas.concat(
        [
            geopandas.read_file(
                "https://www2.census.gov/geo/tiger/TIGER"
                + year
                + "/TRACT/tl_"
                + year
                + "_"
                + state
                + "_tract.zip"
            )
            for state in states
        ]
    )
    geometry.STATEFP = geometry.STATEFP.apply(int)
    geometry.COUNTYFP = geometry.COUNTYFP.apply(int)
    geometry.TRACTCE = geometry.TRACTCE.apply(int)
    return geometry
