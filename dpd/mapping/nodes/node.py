class Node:
    def __init__(self, geometry):
        self.geometry = geometry
        self.entry_velocity = None

    def new_approaching_body(self, body):
        body.end_current_node()

