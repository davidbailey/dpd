from math import sqrt


def circle_center_from_points_and_radius(point1, point2, radius, right_handed):
    """
    Finds the center of a circle with a given radius such that point1 and point2 are on the circumference of the circle.
    Based on https://stackoverflow.com/questions/36211171/finding-center-of-a-circle-given-two-points-and-radius.
    There can be three possible outcomes: no solutions, one solution, or two solutions.
    If there are no solutions (e.g. radius is less than half the distance between the points), a "ValueError: math domain error" will raise.
    If there is one solution, right_handed does not matter.
    If there are two solutions, use right_handed to choose solution the solution. The arc length of the solutions are very close.
    """
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]

    q = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    y3 = (y1 + y2) / 2
    x3 = (x1 + x2) / 2

    base_x = sqrt(radius**2 - (q / 2) ** 2) * (y1 - y2) / q
    base_y = sqrt(radius**2 - (q / 2) ** 2) * (x2 - x1) / q

    if right_handed:
        center_x2 = x3 - base_x
        center_y2 = y3 - base_y
        return [center_x2, center_y2]
    else:
        center_x1 = x3 + base_x
        center_y1 = y3 + base_y
        return [center_x1, center_y1]
