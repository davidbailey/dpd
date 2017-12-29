import requests
import geopandas
from shapely.geometry import asShape
from shapely import ops
from functools import partial
import pyproj
import concurrent.futures
import pandas

def get_uscensus_data_by_tract(year, state, county, data={}):
    url = 'https://api.census.gov/data/' + year + '/acs/acs5/profile?get=NAME'
    for datum in data.values():
        url += ',' + datum
    url += '&for=tract:*&in=state:' + state + '&in=county:' + county
    r = requests.get(url)
    tracts = geopandas.GeoDataFrame(r.json()[1:], columns = ['NAME'] + list(data.keys()) + ['state', 'county', 'tract'], dtype='int')
    return tracts

def get_uscensus_geometry(state, county, tract):
    url = 'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Tracts_Blocks/MapServer/0/query?f=geojson&where=state%3D' + state + '+and+county%3D' + county + '+and+tract%3D' + str(tract)
    r = requests.get(url)
    featureGeoJSON = r.json()['features'][0]['geometry']
    featureShapely = asShape(featureGeoJSON)
    return featureShapely


def add_density_to_tracts(row):
    polygon = ops.transform(partial(pyproj.transform, pyproj.Proj(init='EPSG:4326'), pyproj.Proj(proj='aea')), row['geometry'])
    density = 1000000 * row['Total Population'] / polygon.area
    return density


def get_uscensus_density_by_tract(year, state, county):
    tracts = get_uscensus_population_by_tract(year=year, state=state, county=county)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor: # The API is a bit slow so we parallelize
        geometry = executor.map(partial(get_uscensus_geometry, state, county), tracts['tract'])
    tracts['geometry'] = pandas.Series(geometry, index=tracts.index)
    tracts['density'] = tracts.apply(add_density_to_tracts, axis=1)
    return tracts
