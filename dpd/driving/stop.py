from astropy import units
from geopandas import GeoDataFrame
import geojsoncontour
import json
from matplotlib import pyplot as plt
import numpy as np
from shapely.geometry import Point

from dpd.osrm import table

speed = {
    "walking": 1.35 * units.meter / units.second,
    "cycling": 5 * units.meter / units.second,
}


class Stop:
    """
    A class to describe a stop along a Route.
    """

    def __init__(self, geometry):
        self.geometry = geometry

    def accessibility(self, x, y, mode, how="constant_speed"):
        if how == "constant_speed":
            z = []
            for x_ in x:
                for y_ in y:
                    z.append(
                        (
                            self.geometry.distance(Point(x_, y_))
                            * units.meter
                            / speed[mode]
                        )
                        .to(units.second)
                        .value
                    )
        elif how == "osrm":
            origins = str(self.geometry.x) + "," + str(self.geometry.y)
            destinations = ""
            for x_ in x:
                for y_ in y:
                    destinations += ";" + str(x_) + "," + str(y_)
            response = table(origins, destinations, mode=mode, options="?sources=0")
            z = response["durations"][0][1:]
        z = np.array(z).reshape([len(x), len(y)])
        return z

    def accessibility_grid(self, time, mode, how="constant_speed"):
        x = np.linspace(
            self.geometry.coords[0][0] - (speed[mode] * time).to(units.meter).value,
            self.geometry.coords[0][0] + (speed[mode] * time).to(units.meter).value,
        )
        y = np.linspace(
            self.geometry.coords[0][1] - (speed[mode] * time).to(units.meter).value,
            self.geometry.coords[0][1] + (speed[mode] * time).to(units.meter).value,
        )
        z = accessibility(x, y, mode, how)
        return x, y, z

    def accessibility_contourf(self, times, mode, how="constant_speed"):
        x, y, z = self.accessibility_grid(times[-1], mode, how)
        fig, ax = plt.subplots(1)
        levels = list(map(lambda x: x.to(units.second).value, times))
        contourf = ax.contourf(x, y, z, levels=levels, extend="min")
        plt.close()
        return contourf

    def accessibility_contourf_geojson(self, times, mode, how="constant_speed"):
        contourf = self.accessibility_contourf(times, mode, how)
        return json.loads(geojsoncontour.contourf_to_geojson(contourf))

    def accessibility_contourf_features(
        self, times, mode, how="constant_speed", crs=None
    ):
        return GeoDataFrame.from_features(
            self.accessibility_contourf_geojson(times, mode, how)["features"], crs=crs
        )

    def accessibility_radius(self, time, mode):
        return self.geometry.buffer((speed[mode] * time).to(units.meter).value)

    def accessibility_radius_features(self, times, mode, crs=None):
        features = []
        for time in times:
            features.append({"geometry": self.accessibility_radius(time, mode)})
        return GeoDataFrame(features, crs=crs)
