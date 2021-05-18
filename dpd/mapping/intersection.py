class Intersection:
    """
    Intersection: a place where things intersect.

    input_lanes are lanes which feed into the intersection.
    output_lanes are lanes which feed out of the intersection.
    """

    def __init__(self, name, geometry, input_links=None, output_links=None, **kwargs):
        self.name = name
        self.geometry = geometry
        if input_links:
            self.input_links = input_links
        else:
            self.input_links = []
        if output_links:
            self.output_links = output_links
        else:
            self.output_links = []
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def add_input_link(self, input_link):
        self.input_links.append(input_link)

    def add_output_link(self, output_link):
        self.output_links.append(output_link)
