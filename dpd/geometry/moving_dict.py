from .geometric_dict import GeometricDict
from movingpandas import Trajectory


class MovingDict(GeometricDict):
    """
    A dictionsary of objects with a .geometry and a datetime index.
    """

    def __init__(self, dict=None, crs=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_trajectory(self, traj_id, columns=["geometry"], *args, **kwargs):
        geodataframe = self.to_geodataframe(columns=columns)
        return Trajectory(geodataframe, traj_id, *args, **kwargs)
