import numpy

from .find_center_from_points_and_radius import find_center_from_points_and_radius

def draw_arc(start_point, end_point, radius, right_handed, number_of_points):
    """
    Returns an array of points from start_point to end_point along the circumference of a circle with a given radius
    """
    center = find_center_from_points_and_radius(start_point, end_point, radius, right_handed=right_handed)
    chord = numpy.linspace([start_point.x, start_point.y], [end_point.x, end_point.y], number_of_points)
    vectors = chord - center
    magnitudes = numpy.linalg.norm(vectors, axis=1)
    factors = radius / magnitudes
    return (vectors.T * factors).T + center
