from .route import Route

class Network:
    """
    a transporation network with multiple routes
    """

    def __init__(routes):
        self.routes = routes
        
    def from_gtfs(feed):
        pass

    def from_osm_relations(relations):
        routes = []
        for relation in relations:
            routes.append(Route.from_osm_relation(relation))
        return Network(routes)

    def plot_folium(self, folium_map):
        pass
