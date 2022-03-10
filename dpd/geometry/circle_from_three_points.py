from math import sqrt


def circle_from_three_points(p0, p1, p2):
    """
    Calculates the center and radius of a circle from three points on the circumference of the circle.
    Based on https://www.geeksforgeeks.org/equation-of-circle-when-three-points-on-the-circle-are-given/
    Args:
        p0 (float, float): the coordinates of a point on the circumference of the circle
        p1 (float, float): the coordinates of a point on the circumference of the circle
        p2 (float, float): the coordinates of a point on the circumference of the circle
    Returns:
        (x,y), r: (x,y) are the coordinates of the center of the circle; r is the radius of the circle
    """
    x1, y1 = p0
    x2, y2 = p1
    x3, y3 = p2

    x12 = x1 - x2
    x13 = x1 - x3
    y12 = y1 - y2
    y13 = y1 - y3
    y31 = y3 - y1
    y21 = y2 - y1
    x31 = x3 - x1
    x21 = x2 - x1

    sx13 = x1**2 - x3**2
    sy13 = y1**2 - y3**2
    sx21 = x2**2 - x1**2
    sy21 = y2**2 - y1**2

    f = (sx13 * x12 + sy13 * x12 + sx21 * x13 + sy21 * x13) / (
        2 * (y31 * x12 - y21 * x13)
    )
    g = (sx13 * y12 + sy13 * y12 + sx21 * y13 + sy21 * y13) / (
        2 * (x31 * y12 - x21 * y13)
    )
    c = -(x1**2) - y1**2 - 2 * g * x1 - 2 * f * y1

    h = -g
    k = -f
    r = sqrt(h**2 + k**2 - c)
    return (h, k), r
