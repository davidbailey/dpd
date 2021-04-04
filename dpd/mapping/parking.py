class Parking:
    def __init__(self, link, type_):
        self.link = link
        allowed_parking_types = ["parallel", "angle", "reverse-angle", "perpendicular"]
        if type_ not in allowed_parking_types:
            raise ValueError("Parking type must be from %s" % (allowed_parking_types))
        self.type_ = type_
