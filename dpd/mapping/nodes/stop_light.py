from .node import Node


class StopLight(Node):
    """
    🚦🚥
    """

    def __init__(self, signal_plan, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def new_approaching_body(self, body):
        body.end_current_node()

    def step(self):
        pass
