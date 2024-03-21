from numpy import minimum

from .edges_lanes_driver import EdgesLanesDriver


class EdgesLanesNodesDriver(EdgesLanesDriver):
    def __init__(self, nodes, *args, **kwargs):
        self.nodes = nodes
        self.waiting_at_node = False
        self.begin_next_node()
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_node_ids(edges_dict, nodes_dict, node_ids, *args, **kwargs):
        """
        Preplans the nodes and edges for a Driver based on Node IDs and a nodes_dict and edges_dict
        
        edges_dict (dict): a dictionary with a tuple of (node_id[i], node_id[i+1] as the index for each edge value, this is often a networkx.DiGraph.edges or a pandas.DataFrame
        nodes_dict (dict): a dictionary with node_id as the index for each node value, this is often a networkx.DiGraph.nodes or a pandas.DataFrame
        node_ids ([node_id]): a list of Node IDs that describes the route a Driver takes
        """
        edges = [
            edges_dict[(node_ids[i], node_ids[i + 1])]["object"] for i in range(len(node_ids) - 1)
        ]
        nodes = [nodes_dict[node_id]["object"] for node_id in node_ids]
        return EdgesLanesNodesDriver(edges=edges, nodes=nodes, *args, **kwargs)

    def begin_next_edge(self, *args, **kwargs):
        super().begin_next_edge(*args, **kwargs)
        if self.next_node.entry_velocity is not None:
            self.body.final_velocity = minimum(
                self.body.final_velocity, self.next_node.entry_velocity
            )

    def end_current_edge(self, *args, **kwargs):
        if not self.waiting_at_node:
            self.waiting_at_node = True
            self.next_node.new_approaching_body(self)

    def begin_next_node(self):
        self.next_node = self.nodes.pop(0)

    def end_current_node(self):
        self.waiting_at_node = False
        self.begin_next_node()
        super().end_current_edge(
            extra_position=None
        )  # update this in cases where the driver does not stop
