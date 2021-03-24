import datetime
import logging


from astropy import units
import folium
import geopandas as gpd
from matplotlib import pyplot as plt
import movingpandas as mpd
import numpy as np
from pyproj import CRS
import requests
from shapely.geometry import box
from tqdm import tqdm


from dpd.mapping import Map
from dpd.werkzeug import WerkzeugThread
from .driver import Driver
from .people_flask_app import people_flask_app
from .yieldintersection import YieldIntersection

SignalIntersection = YieldIntersection
StopIntersection = YieldIntersection


class ABTMMap(Map):
    def __init__(self, model, map_):
        self.model = model
        self.intersections = map_.intersections
        self.roads = map_.roads
        self.people = gpd.GeoDataFrame(columns=["geometry", "Person"])
        self.intersections["Intersection"] = self.intersections.apply(
            self.transform_intersection_to_agent_based,
            axis=1,
        )
        self.roads.apply(self.transform_road_to_agent_based, axis=1)
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
            elif intersection_type == "Stop":
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
        if "maxspeed" in road.index:
            road["Road"].max_speed = road["maxspeed"]
        else:
            road["Road"].max_speed = 1 * units.meter / units.second
        if road["Road"].input_intersection:
            road["Road"].input_intersection = self.intersections.loc[
                road["Road"].input_intersection.name
            ]["Intersection"]
        if road["Road"].output_intersection:
            road["Road"].output_intersection = self.intersections.loc[
                road["Road"].output_intersection.name
            ]["Intersection"]

    def clear_lanes(self):
        """
        adds occupants to all lanes. can also be run later to clear lanes of occupants from past model
        """
        for road in self.roads["Road"]:
            for lane in road.lanes:
                if lane is not None:
                    lane.occupants = []

    def nodes_to_roads(self, node_ids):
        """Takes a list of node_ids and a map and returns a list or roads."""
        nodes = []
        # first we filter through all the nodes and find those that are actually intersections. for those that are not intersections, we assume they are part of the roads. this may or may not be true.
        for node in node_ids:
            if node in self.intersections.index:
                nodes.append(node)
        roads = []
        for i in range(len(nodes) - 1):
            for road in self.intersections.loc[nodes[i]]["Intersection"].output_roads:
                if (
                    road.output_intersection
                    and road.output_intersection.name == nodes[i + 1]
                ):
                    roads.append(road)
                    break
        return roads

    def create_people_from_od(self, od):
        people = {}
        for _, person in tqdm(od.iterrows(), total=len(od)):
            route = self.nodes_to_roads(
                person.routes[0]["legs"][0]["annotation"]["nodes"]
            )
            # todo - add other modes
            driver = Driver(self.model, person.home_geometry, route)
            people[driver.name] = {"geometry": driver.geometry, "Person": driver}
            self.model.schedule.add(driver)
        self.people = gpd.GeoDataFrame.from_dict(people, orient="index")
        self.people.crs = "EPSG:4326"

    def transform_people_to_aea(self):
        logging.info("Transforming people to AEA. This could take a while...")
        aea = CRS.from_string("North America Albers Equal Area Conic")
        self.people.to_crs(aea, inplace=True)
        for _, person in self.people.iterrows():
            person["Person"].geometry = person["geometry"]

    def transform_people_to_epsg4326(self):
        self.people.to_crs("EPSG:4326", inplace=True)
        for _, person in self.people.iterrows():
            person["Person"].geometry = person["geometry"]

    def post_people(self, url):
        self.refresh_people_geometries()
        crs = self.people.crs
        self.people.to_crs("EPSG:4326", inplace=True)
        p = requests.post(url, data={"people": self.people["geometry"].to_json()})
        self.people.to_crs(crs, inplace=True)

    def refresh_people_geometries(self):
        self.people["geometry"] = self.people["Person"].map(
            lambda person: person.geometry
        )

    def all_people_arrived(self):
        for person in self.people["Person"]:
            if not person.arrived:
                return Fasle
        return True

    def simulate(
        self,
        number_of_rounds=np.inf,
        time=datetime.datetime(1970, 1, 1, 0, 0, 0),
        post_people=False,
    ):
        trajectories = []
        if not self.intersections.crs == CRS.from_string(
            "North America Albers Equal Area Conic"
        ):
            self.transform_intersections_to_aea()
        if not self.roads.crs == CRS.from_string(
            "North America Albers Equal Area Conic"
        ):
            self.transform_roads_to_aea()
        if not self.people.crs == CRS.from_string(
            "North America Albers Equal Area Conic"
        ):
            self.transform_people_to_aea()
        if post_people:
            werkzeug_thread = WerkzeugThread(people_flask_app())
            werkzeug_thread.start()
        round_number = 0
        while round_number <= number_of_rounds and not self.all_people_arrived():
            logging.info("Simulating round %s" % (round_number,))
            for _, person in self.people.iterrows():
                if not person["Person"].arrived:
                    trajectories.append(
                        {
                            "time": time,
                            "geometry": person["Person"].geometry,
                            "name": person.name,
                        }
                    )
            if post_people:
                self.post_people("http://localhost:9000/people")
            self.model.step()
            time = time + datetime.timedelta(seconds=1)
            round_number = round_number + 1
        if post_people:
            werkzeug_thread.stop()
        gpd_trajectories = gpd.GeoDataFrame(trajectories).set_index("time")
        gpd_trajectories.crs = CRS.from_string("North America Albers Equal Area Conic")
        gpd_trajectories.to_crs("EPSG:4326", inplace=True)
        mpd_trajectories = mpd.TrajectoryCollection(gpd_trajectories, "name")
        return mpd_trajectories

    def plot(
        self,
        include_intersections=False,
        include_roads=False,
        include_people=True,
        filter_box=None,
    ):
        fig = plt.figure(figsize=(18, 16))
        ax = fig.add_subplot(111)
        if filter_box:
            filter_df = GeoDataFrame(Polygon(box(filter_box)), columns=["geometry"])
            filter_df = "EPSG:4326"
        else:
            filter_df = None
        if include_intersections:
            self.plot_df(ax, self.intersections, filter_df)
        if include_roads:
            self.plot_df(ax, self.roads, filter_df)
        if include_people:
            self.plot_df(ax, self.people, filter_df)
        plt.show()

    def plot_folium_people(self, folium_map, fields_people):
        if fields_people:
            geojson = folium.GeoJson(
                self.people[["geometry"]],
                tooltip=folium.features.GeoJsonTooltip(fields=fields_people),
            )
        else:
            geojson = folium.GeoJson(self.people[["geometry"]])
        geojson.add_to(folium_map)

    def plot_folium(
        self,
        include_intersections=False,
        include_roads=False,
        include_people=True,
        folium_map=None,
        fields_intersections=None,
        fields_roads=None,
        fields_people=None,
        filter_box=None,
    ):
        if not folium_map:
            folium_map = folium.Map(location=(38.9, -77), zoom_start=12)
        if filter_box:
            filter_df = GeoDataFrame(Polygon(box(filter_box)), columns=["geometry"])
            filter_df = "EPSG:4326"
        else:
            filter_df = None
        if include_roads:
            self.plot_folium_df(folium_map, self.roads, filter_df, fields_roads)
        if include_intersections:
            self.plot_folium_df(
                folium_map, self.intersections, filter_df, fields_intersections
            )
        if include_people:
            self.plot_folium_df(folium_map, self.people, filter_df, fields_people)
        return folium_map
