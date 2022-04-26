import logging

from astropy import units
from pandas import Series, isna, read_csv

from dpd.driving import Vehicle


class Vehicles(Series):
    def read_csv(
        url,
        default_power,
        default_mass,
        default_max_speed,
        default_acceleration_limit,
        default_max_deceleration,
    ):
        dataframe = read_csv(url)
        dataframe.index = dataframe.Manufacturer + " " + dataframe.Model
        dataframe.sort_index(inplace=True)
        vehicles = []
        for index, row in dataframe.iterrows():
            logging.debug("Adding %s" % (index,))
            power = (
                row["Power"].split(" ")[0] * units.Unit(row["Power"].split(" ")[1])
                if not isna(row["Power"])
                else default_power
            )
            mass = (
                row["Mass"].split(" ")[0] * units.Unit(row["Mass"].split(" ")[1])
                if not isna(row["Mass"])
                else default_mass
            )
            max_speed = (
                row["Maximum speed"].split(" ")[0]
                * units.Unit(row["Maximum speed"].split(" ")[1])
                if not isna(row["Maximum speed"])
                else default_max_speed
            )
            acceleration_limit = (
                row["Acceleration"].split(" ")[0]
                * units.Unit(row["Acceleration"].split(" ")[1])
                if not isna(row["Acceleration"])
                else default_acceleration_limit
            )
            max_deceleration = (
                row["Deceleration"].split(" ")[0]
                * units.Unit(row["Deceleration"].split(" ")[1])
                if not isna(row["Deceleration"])
                else default_max_deceleration
            )
            vehicles.append(
                Vehicle(
                    power=power,
                    mass=mass,
                    max_speed=max_speed,
                    acceleration_limit=acceleration_limit,
                    max_deceleration=max_deceleration,
                )
            )
        return Series(data=vehicles, index=dataframe.index)
