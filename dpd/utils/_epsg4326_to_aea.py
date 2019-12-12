"""
epsg4326_to_aea: transform a geom from EPSG:4326 to Albers Equal Area
"""
from pyproj import CRS, Transformer
from shapely.ops import transform


def epsg4326_to_aea(geom):
    """
    epsg4326_to_aea: transform a geom from EPSG:4326 to Albers Equal Area
    """
    crs_4326 = CRS.from_epsg(4326)
    aea = CRS.from_string("North America Albers Equal Area Conic")
    transformer = Transformer.from_crs(crs_4326, aea, always_xy=True)
    return transform(transformer.transform, geom)
