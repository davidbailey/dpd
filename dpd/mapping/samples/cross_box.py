from itertools import combinations

from networkx import DiGraph
from shapely.geometry import LineString, Point

graph = DiGraph()

i = 0
nodes = []

for x in range(2):
    for y in range(2):
        nodes.append((i, {"geometry": Point(x, y), "type": "stop_sign"}))
        i += 1

graph.add_nodes_from(nodes)

edges = []
for node_origin, node_destination in combinations(graph.nodes, 2):
    geometry = LineString(
        [
            graph.nodes[node_origin]["geometry"],
            graph.nodes[node_destination]["geometry"],
        ]
    )
    edges.append(
        (
            node_origin,
            node_destination,
            {
                "geometry": geometry,
                "length": geometry.length,
                "lanes": 1,
                "maxspeed": 10,
            },
        )
    )
    geometry = LineString(
        [
            graph.nodes[node_destination]["geometry"],
            graph.nodes[node_origin]["geometry"],
        ]
    )
    edges.append(
        (
            node_destination,
            node_origin,
            {
                "geometry": geometry,
                "length": geometry.length,
                "lanes": 1,
                "maxspeed": 10,
            },
        )
    )


graph.add_edges_from(edges)
