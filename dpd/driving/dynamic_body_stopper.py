from .kinematic_body_with_acceleration_stopper import (
    KinematicBodyWithAccelerationStopper,
)
from .dynamic_body_driver import DynamicBodyDriver


class DynamicBodyStopper(DynamicBodyDriver, KinematicBodyWithAccelerationStopper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
