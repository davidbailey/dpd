import folium
import geopandas as gpd
from matplotlib import pyplot as plt


from dpd.mapping import Map
from .yieldintersection import YieldIntersection


class ABTMMap(Map):
    def __init__(self, model, map_):
        self.model = model
        self.intersections = map_.intersections
        self.roads = map_.roads
        self.people = gpd.GeoDataFrame(columns=["geometry", "Person"])
        self.intersections["Intersection"] = self.intersections.apply(
            lambda intersection: self.transform_intersection_to_agent_based(
                intersection
            ),
            axis=1,
        )
        self.roads["Road"].map(lambda road: self.transform_road_to_agent_based(road))
        self.clear_lanes()

    def add_person(self, person):
        self.people.loc[person.name] = [
            person.geometry,
            person,
        ]
        self.model.schedule.add(person)

    def transform_intersection_to_agent_based(self, intersection):
        if hasattr(intersection, "Type"):
            intersection_type = intersection["Type"]
            if intersection_type == "Signal":
                intersection = SignalIntersection(
                    intersection["Intersection"], self.model
                )
            elif intersection_type == "Yield":
                intersection = StopIntersection(
                    intersection["Intersection"], self.model
                )
            else:
                intersection = YieldIntersection(
                    intersection["Intersection"], self.model
                )
        else:
            intersection = YieldIntersection(intersection["Intersection"], self.model)
        self.model.schedule.add(intersection)
        return intersection

    def transform_road_to_agent_based(self, road):
        """
        this must be run after transform_intersection_to_agent_based creates new Intersection objects.
        """
        if road.input_intersection:
            road.input_intersection = self.intersections.loc[
                road.input_intersection.name
            ]["Intersection"]
        if road.output_intersection:
            road.output_intersection = self.intersections.loc[
                road.output_intersection.name
            ]["Intersection"]

    def clear_lanes(self):
        """
        adds occupants to all lanes. can also be run later to clear lanes of occupants from past model
        """
        for road in self.roads["Road"]:
            for lane in road.lanes:
                if lane is not None:
                    lane.occupants = []

    def refresh_people_geometries(self):
        self.people["geometry"] = self.people["Person"].map(
            lambda person: person.geometry
        )

    def abtmplot(self, include_intersections=False, include_roads=False):
        self.refresh_people_geometries()
        fig = plt.figure(figsize=(18, 16))
        ax = fig.add_subplot(111)
        self.people.plot(ax=ax)
        for idx, row in self.people.iterrows():
            plt.annotate(
                text=idx,
                xy=row.geometry.centroid.coords[0],
                horizontalalignment="center",
            )
        self.plot(
            fig=fig,
            ax=ax,
            include_intersections=include_intersections,
            include_roads=include_roads,
        )

    def abtmplot_folium(
        self, include_intersections=False, include_roads=False, fields_people=None
    ):
        self.refresh_people_geometries()
        folium_map = folium.Map(location=(38.9, -77), zoom_start=12)
        self.people.crs = "EPSG:4326"
        if fields_people:
            geojson = folium.GeoJson(
                self.people[["geometry"]],
                tooltip=folium.features.GeoJsonTooltip(fields=fields_people),
            )
        else:
            geojson = folium.GeoJson(self.people[["geometry"]])
        geojson.add_to(folium_map)
        return self.plot_folium(
            folium_map=folium_map,
            include_intersections=include_intersections,
            include_roads=include_roads,
        )
