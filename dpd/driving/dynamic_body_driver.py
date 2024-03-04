from dpd.mechanics import DynamicBody

from .kinematic_body_with_acceleration_driver import KinematicBodyWithAccelerationDriver


class DynamicBodyDriver(DynamicBody, KinematicBodyWithAccelerationDriver):
    pass
