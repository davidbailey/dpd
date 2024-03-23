from .node import Node
from .stop import Stop
from .stop_light import StopLight
from .stop_sign import StopSign
from .yield_sign import YieldSign


def object_for_node(node):
    """
    node

    """
    if node.get("type") == "stop_sign":
        return StopSign(geometry=node["geometry"])
    elif node.get("type") == "yield_sign":
        return YieldSign(geometry=node["geometry"])
    elif node.get("type") == "stop_light":
        return StopLight(geometry=node["geometry"])
    elif node.get("type") == "stop":
        return Stop(geometry=node["geometry"], dwell_time=node["dwell_time"])
    else:
        return Node(geometry=node["geometry"])
