import folium
import geopandas as gpd
from matplotlib import pyplot as plt

from dpd.geopandas import filter_geodataframe


class GeoObjectDataFrame(gpd.GeoDataFrame):
    """
    A base class for Links and Intersections.
    """

    def __init__(self, *args, **kwargs):
        if not "columns" in kwargs.keys():
            super().__init__(columns=["geometry", "object"], *args, **kwargs)
        else:
            super().__init__(*args, **kwargs)

    def add_object(self, object_):
        self.loc[object_.name] = [
            object_.geometry,
            object_,
        ]

    def transform_crs(crs):
        # CRS.from_string("North America Albers Equal Area Conic")
        # "EPSG:4326"
        self.to_crs(crs, inplace=True)
        for _, object_ in self.iterrows():
            object_["object"].geometry = object_["geometry"]

    def plot_with_labels(self, ax, filter_box=None, **kwargs):
        if filter_box:
            plot_gdf = filter_geodataframe(self, filter_box)
        else:
            plot_gdf = self
        plot_gdf.plot(ax=ax, **kwargs)
        for idx, row in plot_gdf.iterrows():
            plt.annotate(
                text=idx,
                xy=row.geometry.centroid.coords[0],
                horizontalalignment="center",
            )

    def plot_folium(self, folium_map, filter_box=None, **kwargs):
        if filter_box:
            plot_gdf = filter_geodataframe(self, filter_box)
        else:
            plot_gdf = self
        if not "name" in plot_gdf.columns:
            plot_gdf["name"] = plot_gdf["object"].map(lambda object_: object_.name)
        tooltip = folium.features.GeoJsonTooltip(fields=["name"])
        geojson = folium.GeoJson(
            plot_gdf[["name", "geometry"]].to_json(), tooltip=tooltip, **kwargs
        )
        geojson.add_to(folium_map)
