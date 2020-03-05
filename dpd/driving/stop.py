from shapely.geometry import Point

class Stop:
    def __init__(self, location, name = ""):
        """
        Defines a public transportation stop
        """
        self.location:Point = location
        self.name:str = name
