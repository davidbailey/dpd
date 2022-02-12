from .geometric_dict import GeometricDict
from movingpandas import Trajectory

class MovingDict(GeometricDict):
    """
    A dictionsary of objects with a .geometry and a .t (datetime)
    """

    def __init__(self, dict=None, crs=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_trajectory(self, traj_id, *args, **kwargs):
        geodataframe = self.to_geodataframe()
        return Trajectory(geodataframe, traj_id, *args, **kwargs)
    
    def to_geodataframe(self, columns=["geometry", "t"]):
        return super().to_geodataframe(columns=columns, *args, **kwargs)

    def to_json(self, columns=["geometry", "t"]):
        return super().to_json(columns=columns, *args, **kwargs)
