from mesa import Agent
from uuid import uuid4


from dpd.mapping import Intersection


class YieldIntersection(Agent, Intersection):
    """
    Every intersection must have a step(self) method which gets called by the simulation and a new_approach(self, approacher) method which gets called by an approacher.
    An approacher is anything that approaches the intersection. When it is safe, the intersection will call the approacher.proceed_through_intersection() on the approacher and then it is up to the approacher to proceed to the next lane.
    The base class here implements no delay and is only realistic for one input to one output lane.
    """

    def __init__(self, intersection, model):
        unique_id = uuid4()
        Agent.__init__(self, unique_id, model)
        Intersection.__init__(
            self,
            intersection.name,
            intersection.geometry,
            intersection.input_roads,
            intersection.output_roads,
        )

    def new_approach(self, approacher):
        approacher.proceed_through_intersection()
