import folium

from .geoobjectdataframe import GeoObjectDataFrame


class Links(GeoObjectDataFrame):
    """
    A class to hold Links.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def plot_folium(self, folium_map, filter_box=None, **kwargs):
        if filter_box:
            plot_gdf = filter_geodataframe(self, filter_box)
        else:
            plot_gdf = self
        if not "name" in plot_gdf.columns:
            plot_gdf["name"] = plot_gdf["object"].map(lambda link: link.name)
        if not "number_of_segments" in plot_gdf.columns:
            plot_gdf["number_of_segments"] = plot_gdf["object"].map(
                lambda link: len(link.segments) - 2
            )
        if not "segments" in plot_gdf.columns:
            plot_gdf["segments"] = plot_gdf["object"].map(
                lambda link: str(list(map(type, link.segments)))
            )
        style_function = lambda x: {"weight": x["properties"]["number_of_segments"]}
        tooltip = folium.features.GeoJsonTooltip(fields=["name", "segments"])
        geojson = folium.GeoJson(
            plot_gdf[["name", "geometry", "number_of_segments", "segments"]].to_json(),
            tooltip=tooltip,
            style_function=style_function,
            **kwargs
        )
        geojson.add_to(folium_map)
