from astropy import units
import numpy as np
from shapely.geometry import Point

speed = {
    "walking": 1.35 * units.meter / units.second,
    "cycling": 5 * units.meter / units.second
}

class Stop:
    """
    A class to describe a stop along a Route.
    """

    def __init__(self, geometry):
        self.geometry = geometry

    def accessibility_contour(self, time, mode, method="simple"):
        origins = uniform_points_in_polygon(self.accessibility_radius(time, mode))
        x = np.linspace(self.geometry.coords[0][1] - (speed[mode] * time).value, self.geometry.coords[0][1] + (speed[mode] * time).value)
        y = np.linspace(self.geometry.coords[0][0] - (speed[mode] * time).value, self.geometry.coords[0][0] + (speed[mode] * time).value)
        z = []
        if method="simple":
            for x_ in x:
                for y_ in y:
                    z.append(self.geometry.distance(Point(x_, y_)))
            z = np.array(z).reshape([len(x), len(y)])
        if method="osrm":
            pass
        return x, y, z
    
    def accessibility_radius(self, time, mode):
        return self.geometry.buffer((speed[mode] * time).value)
