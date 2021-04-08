from collections import UserDict

import folium
from geopandas import GeoDataFrame, GeoSeries
from matplotlib import pyplot as plt
from pyproj import Transformer
from shapely.ops import transform

from dpd.geopandas import filter_geodataframe


class GeometricDict(dict):
    """
    A dictionsary of objects with a .geometry
    """

    def __init__(self, crs=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crs = crs

    def to_crs(self, crs):
        """ Or we could go to_geoseries, to_crs, and then reset... which is faster?"""
        transformer = Transformer.from_crs(self.crs, crs)
        for value in self.values():
            lon, lat = value.geometry.xy
            value.geometry = transformer.transform(lon, lat)
        self.crs = crs

    def to_geoseries(self):
        data = {}
        for key, value in self.items():
            data[key] = value.geometry
        return GeoSeries(data=data, name="geometry", crs=self.crs)

    def to_geodataframe(self, columns=["geometry"]):
        data = {}
        for key, value in self.items():
            data[key] = {}
            for column in columns:
                data[key][column] = getattr(value, column)
        return GeoDataFrame.from_dict(data=data, orient="index", crs=self.crs)

    def to_json(self, columns=["geometry"]):
        gdf = self.to_geodataframe(columns=columns)
        return gdf.to_json()

    def plot(self, columns=["geometry"], filter_box=None, **kwargs):
        gdf = self.to_geodataframe(columns)
        if filter_box:
            plot_gdf = filter_geodataframe(gdf, filter_box)
        else:
            plot_gdf = gdf
        plot_gdf.plot(**kwargs)
        for idx, row in plot_gdf.iterrows():
            plt.annotate(
                text=idx,
                xy=row.geometry.centroid.coords[0],
                horizontalalignment="center",
            )

    def plot_folium(self, folium_map, columns=["geometry"], filter_box=None, **kwargs):
        gdf = self.to_geodataframe(columns)
        gdf["name"] = gdf.index
        if filter_box:
            plot_gdf = filter_geodataframe(gdf, filter_box)
        else:
            plot_gdf = gdf
        tooltip = folium.features.GeoJsonTooltip(fields=["name"])
        geojson = folium.GeoJson(
            plot_gdf[["name", "geometry"]].to_json(), tooltip=tooltip, **kwargs
        )
        geojson.add_to(folium_map)
