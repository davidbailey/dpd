import numpy


def curve_direction(p0, p1, p2):
    p0_p2 = numpy.array(p2) - numpy.array(p0)
    p0_p1 = numpy.array(p1) - numpy.array(p0)
    cross_product = numpy.cross(p0_p2, p0_p1)
    if cross_product < 0:
        return "left_handed"
    elif cross_product > 0:
        return "right_handed"
    else:
        return "straight"
