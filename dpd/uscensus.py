"""
A set of functions to get data from the US Census API
"""
import concurrent.futures
from functools import partial

import geopandas
import requests
from shapely import ops
from shapely.geometry import asShape
import pandas
import pyproj

def get_uscensus_data_by_tract(year, state, county, data):
    url = 'https://api.census.gov/data/' + year + '/acs/acs5/profile?get=NAME'
    for datum in data.values():
        url += ',' + datum
    url += '&for=tract:*&in=state:' + state + '&in=county:' + county
    request = requests.get(url)
    tracts = geopandas.GeoDataFrame(
        request.json()[1:],
        columns=['NAME'] + list(data.keys()) + ['state', 'county', 'tract'],
        dtype='int'
    )
    return tracts


def get_uscensus_geometry(state, county, tract):
    url = 'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Tracts_Blocks/MapServer/0/query?f=geojson&where=state%3D' + state + '+and+county%3D' + county + '+and+tract%3D' + str(tract)
    request = requests.get(url)
    feature_geojson = request.json()['features'][0]['geometry']
    feature_shapely = asShape(feature_geojson)
    return feature_shapely


def get_uscensus_data_with_geometry(year, state, county, data):
    tracts = get_uscensus_data_by_tract(year=year, state=state, county=county, data=data)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor: # The API is a bit slow so we parallelize
        geometry = executor.map(partial(get_uscensus_geometry, state, county), tracts['tract'])
    tracts['geometry'] = pandas.Series(geometry, index=tracts.index)
    return tracts


def add_density_to_tracts(row):
    polygon = ops.transform(
        partial(
            pyproj.transform,
            pyproj.Proj(init='EPSG:4326'),
            pyproj.Proj(proj='aea')
        ),
        row['geometry']
    )
    density = 1000000 * row['Total Population'] / polygon.area
    return density
