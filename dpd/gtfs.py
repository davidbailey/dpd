import requests
import gtfstk
import tempfile
import folium
import mplleaflet
import geopandas
import numpy
from matplotlib import pyplot
from shapely.geometry import Point
from functools import partial

def url2gtfs(url):
    r = requests.get(url)
    with tempfile.NamedTemporaryFile() as f:
      f.write(r._content)
      return gtfstk.read_gtfs(f.name, dist_units='mi')


def get_rail_stops(gtfs):
    rail_stops = []
    for route_id in gtfs.routes[gtfs.routes['route_type'] == 0]['route_id']:
        for trip_id in gtfs.trips[gtfs.trips['route_id'] == route_id]['trip_id']:
            for stop_id in gtfs.stop_times[gtfs.stop_times['trip_id'] == trip_id]['stop_id']:
                rail_stops.append(stop_id)
    rail_stops = set(rail_stops)
    return gtfs.stops[gtfs.stops['stop_id'].isin(rail_stops)]


def contour_plot(ax, point, resolution, number):
    x = numpy.linspace(point.x - resolution, point.x + resolution, number)
    y = numpy.linspace(point.y - resolution, point.y + resolution, number)
    url = 'http://localhost:5000/table/v1/walking/' + str(point.x) + ',' + str(point.y)
    for i in x:
        for j in y:
            url += ';' + str(i) + ',' + str(j)
    url += '?sources=0'
    request = requests.get(url)
    durations = request.json()['durations'][0][1:]
    z = numpy.array(durations).reshape([len(x), len(y)])
    ax.contour(x, y, z, levels=[300, 600, 900])


def xy2locations(xy):
    x = xy[0]
    y = xy[1]
    locations = []
    for i in range(len(x)):
        locations.append((y[i], x[i]))
    return locations


def plot_linestring(foliumMap, row):
    folium.PolyLine(locations=xy2locations(row['geometry'].xy), color=row['color']).add_to(foliumMap)


def plot_stops(foliumMap, stops, markercolor):
    fig, ax = pyplot.subplots()
    stops.apply(lambda row: contour_plot(ax, Point(float(row['stop_lon']), float(row['stop_lat'])), .025, 15), axis=1)
    geojson = mplleaflet.fig_to_geojson(fig=fig)
    features = geopandas.GeoDataFrame.from_features(geojson['features'])
    features.apply(partial(plot_linestring, foliumMap), axis=1)
    stops.apply(lambda row: folium.Marker([row['stop_lat'], row['stop_lon']], popup=row['stop_name'], icon=folium.Icon(color=markercolor)).add_to(foliumMap), axis=1)
