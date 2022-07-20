from functools import partial

from astropy import units
import ipywidgets as widgets
from IPython.display import display
from pandas import read_csv


from .dynamic_body_stopper import DynamicBodyStopper

class Vehicles:
    def __init__(self, url):
        self.vehicles = read_csv(url)
        self.vehicles.index = self.vehicles.Manufacturer + " " + self.vehicles.Model
        self.vehicles.sort_index(inplace=True)
        self.vehicles.dropna(axis=0, subset=["Maximum speed", "Power", "Mass"], inplace=True)
        vehicle_widget = widgets.Dropdown(
            options=self.vehicles.index,
            description="Vehicle",
        )
        vehicle_widget.observe(self.vehicle_dropdown_observer, names="value")
        display(vehicle_widget)
        self.vehicle = self.create_vehicle(self.vehicles.index[0])

    def vehicle_dropdown_observer(self, value):
        self.vehicle = self.create_vehicle(value.new)

    def create_vehicle(self, index):
        maximum_speed = self.vehicles.loc[index]["Maximum speed"].split(" ")[0] * units.Unit(
            self.vehicles.loc[index]["Maximum speed"].split(" ")[1]
        )
        power = self.vehicles.loc[index]["Power"].split(" ")[0] * units.Unit(
            self.vehicles.loc[index]["Power"].split(" ")[1]
        )
        mass = self.vehicles.loc[index]["Mass"].split(" ")[0] * units.Unit(
            self.vehicles.loc[index]["Mass"].split(" ")[1]
        )
        return partial(DynamicBodyStopper, maximum_speed=maximum_speed, power=power, mass=mass)
