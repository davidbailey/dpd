import numpy as np
import pandas as pd

from astropy import units


class Vehicle:
    """
    Describes a rail or road vehicle and includes methods to drive it along a line
    """

    def __init__(self, mass, power, max_speed):
        self.mass = mass
        self.power = power
        self.max_speed = max_speed

    def acceleration(self, time):
        return np.sqrt(self.power / (2 * self.mass * time))

    def speed(self, time, initial_speed=0):
        return np.sqrt(2 * self.power * time / self.mass)
        return self.acceleration(time) * time + initial_speed

    def distance(self, time, initial_distance=0):
        return self.speed(time) * time + initial_distance
