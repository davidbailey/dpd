import numpy as np


def radius_of_curvature(p0, p1, p2):
    """
    Calculates the radius of curvurature between three points. Based on https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points and https://en.wikipedia.org/wiki/Degree_of_curvature.
    """
    a = np.array([p1[0] - p2[0], p1[1] - p2[1]])
    b = np.array([p1[0] - p0[0], p1[1] - p0[1]])
    c = np.array([p0[0] - p2[0], p0[1] - p2[1]])
    Dc = np.arccos(a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    radius_of_curvature = np.linalg.norm(c) / (2 * np.sin(Dc / 2))
    return radius_of_curvature
