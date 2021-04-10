from dpd.geometry import GeometricDict
from .transportation_model import TransportationModel


class AgentBasedDict(GeometricDict):
    """
    A dictionary of objects with a .geometry for an agent-based model
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = TransportationModel()
