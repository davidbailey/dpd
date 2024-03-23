from .edge import Edge


def object_for_edge(edge):
    """
    edge

    """
    return Edge(
        geometry=edge["geometry"],
        length=edge["length"],
        lanes=edge["lanes"],
        maxspeed=edge["maxspeed"],
    )
