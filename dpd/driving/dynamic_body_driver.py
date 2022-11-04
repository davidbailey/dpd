import numpy

from dpd.mechanics import DynamicBody
from .kinematic_body_with_acceleration_driver import KinematicBodyWithAccelerationDriver


class DynamicBodyDriver(DynamicBody, KinematicBodyWithAccelerationDriver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
