import requests
from shapely.geometry import LineString
from shapely.geometry import MultiLineString
from shapely.ops import polygonize
from functools import partial

def elements2nodes(elements):
  nodes = {}
  for element in elements:
    if element['type'] == "node":
      nodes[element['id']] = (element['lon'], element['lat'])
  return nodes


def elements2ways(elements, nodes):
  ways = {}
  for element in elements:
    if element['type'] == "way":
      ways[element['id']] = (LineString([nodes[nodeid] for nodeid in element['nodes']]))
  return ways


def wayid2way(ways, way):
  if way['type'] == 'way':
    if way['role'] == 'outer':
      return(ways[way['ref']])


def elements2rels(elements, ways):
  rels = {}
  for element in elements:
    if element['type'] == "relation":
      if element['tags']['type'] == 'boundary':
        multilinestring = MultiLineString(list(filter(bool, map(partial(wayid2way, ways), element['members']))))
        rels[element['id']] = {}
        rels[element['id']]['name'] = element['tags']['name']
        rels[element['id']]['geometry'] = list(polygonize(multilinestring))[0]
  return rels

def query2rels(query, endpoint='http://overpass-api.de/api/interpreter'):
    payload = {"data": query}
    r = requests.post(endpoint, data=payload)
    elements = r.json()['elements']
    nodes = elements2nodes(elements)
    ways = elements2ways(elements, nodes)
    return elements2rels(elements, ways)
