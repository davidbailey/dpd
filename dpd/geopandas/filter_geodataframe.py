import geopandas as gpd
from shapely.geometry import Polygon, LineString, box


def filter_geodataframe(gdf, filter_box):
    """
    "Filter" a GeoDataFrame so that only rows in the filter_box are returned. Very useful for plotting a subsection of a large GeoDataFrame.
    """
    filter_gdf = gpd.GeoDataFrame(
        [Polygon(box(filter_box[0], filter_box[1], filter_box[2], filter_box[3]))],
        columns=["geometry"],
    )
    filter_gdf.crs = gdf.crs
    out_gdf = gpd.overlay(gdf, filter_gdf, how="intersection")
    out_gdf = out_gdf[out_gdf["geometry"] != LineString()]
    out_gdf.index.name = gdf.index.name
    return out_gdf
