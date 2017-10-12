import requests
import geopandas
from shapely.geometry import asShape
from shapely import ops
from functools import partial
import pyproj
import concurrent.futures
import pandas

def get_uscensus_population_by_tract(year, state, county):
    # DP02_0086E is "Total Population" https://api.census.gov/data/2012/acs1/profile/variables/DP02_0086E.json
    url = 'http://api.census.gov/data/' + year + '/acs5/profile?get=NAME,DP02_0086E&for=tract:*&in=state:' + state + '&in=county:' + county
    r = requests.get(url)
    tracts = geopandas.GeoDataFrame(r.json()[1:], columns = r.json()[0], dtype='int')
    tracts.index = tracts.NAME
    return tracts


def get_uscensus_geometry(state, county, tract):
    url = 'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Tracts_Blocks/MapServer/0/query?f=geojson&where=state%3D' + state + '+and+county%3D' + county + '+and+tract%3D' + str(tract)
    r = requests.get(url)
    featureGeoJSON = r.json()['features'][0]['geometry']
    featureShapely = asShape(featureGeoJSON)
    return featureShapely


def add_density_to_tracts(row):
    polygon = ops.transform(partial(pyproj.transform, pyproj.Proj(init='EPSG:4326'), pyproj.Proj(proj='aea')), row['geometry'])
    density = 1000000 * row['DP02_0086E'] / polygon.area
    return density


def get_uscensus_density_by_tract(year, state, county):
    tracts = get_uscensus_population_by_tract(year=year, state=state, county=county)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor: # The API is a bit slow so we parallelize
        geometry = executor.map(partial(get_uscensus_geometry, state, county), tracts['tract'])
    tracts['geometry'] = pandas.Series(geometry, index=tracts.index)
    tracts['density'] = tracts.apply(add_density_to_tracts, axis=1)
    return tracts
