"""
epsg4326_to_aea: transform a geom from EPSG:4326 to Albers Equal Area
"""
from functools import partial

import pyproj
from shapely.ops import transform


def epsg4326_to_aea(geom):
    """
    epsg4326_to_aea: transform a geom from EPSG:4326 to Albers Equal Area
    """
    return transform(
        partial(
            pyproj.transform, pyproj.Proj(init="EPSG:4326"), pyproj.Proj(proj="aea")
        ),
        geom,
    )
