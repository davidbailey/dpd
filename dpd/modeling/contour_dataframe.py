import json

import geojsoncontour
from geopandas import GeoDataFrame, GeoSeries
from matplotlib import pyplot as plt
from numpy import linspace
from shapely.geometry import Point

from .distance_dataframe import DistanceDataFrame


def contour_dataframe(
    point,
    crs=None,
    distance=2000,
    levels=[500, 1000, 1500, 2000],
    num=50,
    distance_dataframe_kwargs=None,
):
    if distance_dataframe_kwargs is None:
        distance_dataframe_kwargs = {}
    points = []
    x = linspace(point.x - distance, point.x + distance, num=num)
    y = linspace(point.y - distance, point.y + distance, num=num)
    for i in x:
        for j in y:
            points.append(Point(i, j))
    distance_dataframe = DistanceDataFrame.from_origins_destinations(
        GeoSeries(points), GeoSeries(point), **distance_dataframe_kwargs
    )
    z = distance_dataframe.to_numpy().reshape([num, num])
    fig, ax = plt.subplots(1)
    contourf = ax.contourf(x, y, z, levels=levels, extend="min")
    plt.close()
    return GeoDataFrame.from_features(
        json.loads(geojsoncontour.contourf_to_geojson(contourf))["features"], crs=crs
    )
