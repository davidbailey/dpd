import numpy as np
from shapely.geometry import Point


def uniform_points_in_polygon(polygon, num=50):
    bbox = polygon.bounds
    points = []
    for i in np.linspace(bbox[0], bbox[2], num=num):
        for j in np.linspace(bbox[1], bbox[3], num=num):
            if polygon.intersects(Point(i, j)):
                points.append(Point(i, j))
    return points
