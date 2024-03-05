import folium

from dpd.geometry import GeometricDict
from dpd.geopandas import filter_geodataframe


class Links(GeometricDict):
    """
    A class to hold Links.
    """

    def plot_folium(
        self, folium_map, columns=["geometry", "segments"], filter_box=None, **kwargs
    ):
        gdf = self.to_geodataframe(columns)
        gdf["name"] = gdf.index
        gdf["number_of_segments"] = gdf["segments"].map(
            lambda segments: len(segments) - 2
        )
        gdf["segment_types"] = gdf["segments"].map(
            lambda segments: str(list(map(type, segments)))
        )
        if filter_box:
            plot_gdf = filter_geodataframe(gdf, filter_box)
        else:
            plot_gdf = gdf
        style_function = lambda x: {  # noqa: E731
            "weight": x["properties"]["number_of_segments"]
        }
        tooltip = folium.features.GeoJsonTooltip(fields=["name", "segment_types"])
        geojson = folium.GeoJson(
            plot_gdf[
                ["name", "geometry", "number_of_segments", "segment_types"]
            ].to_json(),
            tooltip=tooltip,
            style_function=style_function,
            **kwargs,
        )
        geojson.add_to(folium_map)
