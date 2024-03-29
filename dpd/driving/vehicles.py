from functools import partial

import ipywidgets as widgets
from astropy import units
from IPython.display import display
from pandas import read_csv

from dpd.mechanics import DynamicBody


class Vehicles:
    def __init__(self, url, vehicle=None):
        self.vehicles = read_csv(url)
        self.vehicles.index = self.vehicles.Manufacturer + " " + self.vehicles.Model
        self.vehicles.sort_index(inplace=True)
        self.vehicles.dropna(
            axis=0, subset=["Maximum speed", "Power", "Mass"], inplace=True
        )
        vehicle_widget = widgets.Dropdown(
            options=self.vehicles.index,
            description="Vehicle",
        )
        vehicle_widget.observe(self.vehicle_dropdown_observer, names="value")
        display(vehicle_widget)
        if vehicle is None:
            vehicle = self.vehicles.index[0]
        vehicle_widget.value = vehicle
        self.vehicle = self.create_vehicle(vehicle)

    def vehicle_dropdown_observer(self, value):
        self.vehicle = self.create_vehicle(value.new)

    def create_vehicle(self, index):
        max_velocity = int(
            self.vehicles.loc[index]["Maximum speed"].split(" ")[0]
        ) * units.Unit(self.vehicles.loc[index]["Maximum speed"].split(" ")[1])
        power = int(self.vehicles.loc[index]["Power"].split(" ")[0]) * units.Unit(
            self.vehicles.loc[index]["Power"].split(" ")[1]
        )
        mass = int(self.vehicles.loc[index]["Mass"].split(" ")[0]) * units.Unit(
            self.vehicles.loc[index]["Mass"].split(" ")[1]
        )
        return partial(
            DynamicBody,
            max_velocity=max_velocity,
            power=power,
            mass=mass,
        )
