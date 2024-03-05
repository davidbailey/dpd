class Edge(dict):
    """
    Maybe split this into Edge (geometry, length, maxspeed) and EdgeWithLanes (lanes) so you can run a model without traffic
    """

    def __init__(self, geometry, length, lanes, maxspeed, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
        self.geometry = geometry
        self.distance = length
        self.lanes = [[] for lane in range(lanes)]
        self.maxspeed = maxspeed
