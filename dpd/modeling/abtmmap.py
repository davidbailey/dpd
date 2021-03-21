import datetime


from astropy import units
import folium
import geopandas as gpd
from matplotlib import pyplot as plt
import movingpandas as mpd
from pyproj import CRS
import requests
from tqdm import tqdm


from dpd.mapping import Map
from dpd.werkzeug import WerkzeugThread
from .driver import Driver
from .people_flask_app import people_flask_app
from .yieldintersection import YieldIntersection

SignalIntersection = YieldIntersection


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
        # print(nodes)
        for i in range(len(nodes) - 1):
            # print("Finding lane from node", nodes[i], "to node", nodes[i+1])
            for road in self.intersections.loc[nodes[i]]["Intersection"].output_roads:
                # if road.output_intersection:
                #    print(road.output_intersection.name)
                if (
                    road.output_intersection
                    and road.output_intersection.name == nodes[i + 1]
                ):
                    roads.append(road)
                    # print("Found lane:", road.name, "that goes from", road.input_intersection.name, "and goes to", road.output_intersection.name)
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
        print("Transforming people to AEA. This could take a while...")
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

    def simulate(
        self,
        number_of_rounds,
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
            werkzeug_thread = WerkzeugThread(people_flask_app)
            werkzeug_thread.start()
        for x in range(number_of_rounds):
            # print("Simulating round", x)
            for _, person in self.people.iterrows():
                # if not person["Person"].arrived
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
        if post_people:
            werkzeug_thread.stop()
        gpd_trajectories = gpd.GeoDataFrame(trajectories).set_index("time")
        gpd_trajectories.crs = CRS.from_string("North America Albers Equal Area Conic")
        gpd_trajectories.to_crs("EPSG:4326", inplace=True)
        mpd_trajectories = mpd.TrajectoryCollection(gpd_trajectories, "name")
        return mpd_trajectories

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
