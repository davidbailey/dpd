from random import uniform

from shapely.geometry import Point


def random_point_in_polygon(polygon):
    (xmin, ymin, xmax, ymax) = polygon.bounds
    while True:
        x = uniform(xmin, xmax)  # nosec
        y = uniform(ymin, ymax)  # nosec
        point = Point(x, y)
        if point.within(polygon):
            return point
