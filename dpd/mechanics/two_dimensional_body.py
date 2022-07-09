from astropy import units

from .body import Body

class TwoDimensionalBody(Body):
    """
    """

    def __init__(self, initial_position=None, *args, **kwargs):
        initial_position = initial_position if initial_position else (0 * units.meter, 0 * units.meter)
        super().__init__(initial_position=initial_position, *args, **kwargs)
        
