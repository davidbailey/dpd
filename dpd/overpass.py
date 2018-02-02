import requests
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import MultiLineString
from shapely.ops import polygonize, linemerge
from functools import partial

def elements2nodes(elements):
  nodes = {}
  for element in elements:
    if element['type'] == "node":
      nodes[element['id']] = {'geometry': Point(element['lon'], element['lat']), 'name': element.get('tags', {}).get('name', '')}
  return nodes


def elements2ways(elements, nodes):
  ways = {}
  for element in elements:
    if element['type'] == "way":
      ways[element['id']] = (LineString([(nodes[nodeid]['geometry'].coords[0]) for nodeid in element['nodes']]))
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

def query2elements(query, element_type='rels', endpoint='http://overpass-api.de/api/interpreter'):
    payload = {"data": query}
    r = requests.post(endpoint, data=payload)
    elements = r.json()['elements']
    nodes = elements2nodes(elements)
    if element_type == 'nodes':
      return nodes
    ways = elements2ways(elements, nodes)
    if element_type == 'ways':
      return ways
    return elements2rels(elements, ways)


def get_railway(area, name, railway):
    if railway == 'stop':
        element_type = 'nodes'
    else:
        element_type = 'ways'
    query = '''
    [out:json][timeout:60];area(%s)->.searchArea;
    rel["name"="%s"](area.searchArea);
    %s(r);
    %s._["railway"="%s"];
    out;>;out skel qt;
    ''' % (area, name, element_type[:-1], element_type[:-1], railway)
    elements = query2elements(query, element_type=element_type)
    if railway == 'stop':
        return list(elements.values())
    else:
        return [{'geometry': linemerge(list(elements.values())), 'name': name}]

def get_key_value_in_area(area, key, value, endpoint='http://overpass-api.de/api/interpreter'):
    query = '''
    [out:json][timeout:60];
    area(%d)->.searchArea;
    (
    node["%s"="%s"](area.searchArea);
    way["%s"="%s"](area.searchArea);
    relation["%s"="%s"](area.searchArea););
    out body;
    >;
    out skel qt;
    ''' % (area, key, value, key, value, key, value)
    data = {"data": query}
    r = requests.post(endpoint, data=data)
    elements = r.json()['elements']
    nodes = {}
    ways = {}
    relations = {}
    for element in elements:
        if element['type'] == "node":
            nodes[element['id']] = {'geometry': Point(element['lon'], element['lat']), 'element': element}
    for element in elements:
        if element['type'] == "way":
            ways[element['id']] = {'geometry': LineString([(nodes[nodeid]['geometry'].coords[0]) for nodeid in element['nodes']]), 'element': element}
    for element in elements:
        if element['type'] == "relation":
            if element['tags']['type'] == 'boundary':
                multilinestring = MultiLineString(list(filter(bool, map(partial(wayid2way, ways), element['members']))))
                relations[element['id']] = {'geometry': list(polygonize(multilinestring))[0], 'element': element}
            else:
                relations[element['id']] = {'element': element}
    return {'nodes': nodes, 'ways': ways, 'relations': relations}

def query(query, endpoint='http://overpass-api.de/api/interpreter'):
    data = {"data": query}
    r = requests.post(endpoint, data=data)
    elements = r.json()['elements']
    nodes = {}
    ways = {}
    relations = {}
    for element in elements:
        if element['type'] == "node":
            nodes[element['id']] = {'geometry': Point(element['lon'], element['lat']), 'element': element}
    for element in elements:
        if element['type'] == "way":
            ways[element['id']] = {'geometry': LineString([(nodes[nodeid]['geometry'].coords[0]) for nodeid in element['nodes']]), 'element': element}
    for element in elements:
        if element['type'] == "relation":
            if element['tags']['type'] == 'boundary':
                multilinestring = MultiLineString(list(filter(bool, map(partial(wayid2way, ways), element['members']))))
                relations[element['id']] = {'geometry': list(polygonize(multilinestring))[0], 'element': element}
            else:
                relations[element['id']] = {'element': element}
    return {'nodes': nodes, 'ways': ways, 'relations': relations}

