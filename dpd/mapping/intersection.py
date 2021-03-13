class Intersection:
    """
    Intersection: a place where things intersect.

    input_lanes are lanes which feed into the intersection.
    output_lanes are lanes which feed out of the intersection.
    """

    def __init__(self, name, geometry, input_roads=[], output_roads=[]):
        self.name = name
        self.geometry = geometry
        self.input_roads = input_roads
        self.output_roads = output_roads

    def add_input_road(self, input_road):
        self.input_roads.append(input_road)

    def add_output_road(self, output_road):
        self.output_roads.append(output_road)
