from .edges import object_for_edge
from .nodes import object_for_node


def add_object_to_edges_and_nodes(graph):
    """
    Adds Edge and Node objects to each Edge and Node in a Graph

    graph (networkx.Graph): a Graph that describes the transportation network

    """
    for edge in graph.edges:
        graph.edges[edge]["object"] = object_for_edge(graph.edges[edge])
    for node in graph.nodes:
        graph.nodes[node]["object"] = object_for_node(graph.nodes[node])

    return graph
