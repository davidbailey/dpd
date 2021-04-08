import folium

from dpd.geometry import GeometricDict


class Links(GeometricDict):
    """
    A class to hold Links.
    """

    def plot_folium(self, folium_map, columns=["geometry"], filter_box=None, **kwargs):
        gdf = self.to_geodataframe(columns)
        gdf["name"] = gdf.index
        gdf["number_of_segments"] = gdf["object"].map(
            lambda link: len(link.segments) - 2
        )
        gdf["segments"] = gdf["object"].map(
            lambda link: str(list(map(type, link.segments)))
        )
        if filter_box:
            plot_gdf = filter_geodataframe(gdf, filter_box)
        else:
            plot_gdf = gdf
        style_function = lambda x: {"weight": x["properties"]["number_of_segments"]}
        tooltip = folium.features.GeoJsonTooltip(fields=["name", "segments"])
        geojson = folium.GeoJson(
            plot_gdf[["name", "geometry", "number_of_segments", "segments"]].to_json(),
            tooltip=tooltip,
            style_function=style_function,
            **kwargs,
        )
        geojson.add_to(folium_map)
