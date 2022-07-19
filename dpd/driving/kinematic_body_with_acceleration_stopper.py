from .kinematic_body_stopper import KinematicBodyStopper
from .kinematic_body_with_acceleration_driver import KinematicBodyWithAccelerationDriver

class KinematicBodyWithAccelerationStopper(KinematicBodyWithAccelerationDriver, KinematicBodyStopper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

