import logging

from dpd.driving import Schedule

class TransportationAlternative:
    def __init__(
        self,
        route,
        vehicle,
        zones,
        dwell_time,
        start,
        end,
        freq
    ):
        self.dwell_time = dwell_time
        self.route = route
        self.vehicle = vehicle
        self.zones = zones
        logging.debug("Creating drive...")
        self.drive = route.drive(vehicle, dwell_time)
        logging.debug("Creating trip...")
        self.trip = route.trip(vehicle, dwell_time)
        logging.debug("Creating trip_reversed...")
        self.trip_reversed = route.reversed.trip(vehicle, dwell_time)
        logging.debug("Creating schedule...")
        self.schedule = Schedule.from_trip(self.trip, start, end, freq)
        logging.debug("Creating schedule_reversed...")
        self.schedule_reversed = Schedule.from_trip(self.trip_reversed, start, end, freq)
        self.schedule_reversed.reverse_distance()
        logging.debug("Creating accessibility...")
        self.accessibility = zones.accessibility(route)


    def plot_folium(self, folium_map):
        self.zones.plot_density(folium_map)
        self.route.plot_folium(folium_map)


    def plot_schedule(self, ax):
        self.schedule.plot_schedule(ax=ax)
        self.schedule_reversed.plot_schedule(ax=ax)
        self.schedule.trips[list(self.schedule.trips.keys())[0]].plot_schedule(ax=ax)  # to add labels


    def plot_speed_limit(self, ax):
        self.drive.speed_limit.dropna().map(lambda x: x.value).plot(ax=ax)


    def plot_accessibility(self, time):
        self.accessibility[
        self.accessibility["time"] < (time).to(units.second).value
        ].groupby("stop").sum()["population"].plot(
            kind="bar",
            title="Population within %s walk of each stop" % (time,),
            ylabel="Population",
            ax=ax,
        )
