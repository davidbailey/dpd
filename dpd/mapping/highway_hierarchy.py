from astropy.units import hour
from astropy.units.imperial import mile

HIGHWAY_HIERARCHY = {  # https://wiki.openstreetmap.org/wiki/Key:highway
    "motorway": {"default_lanes": 4, "default_maxspeed": 55 * mile / hour},
    "motorway_link": {"default_lanes": 4, "default_maxspeed": 55 * mile / hour},
    "trunk": {"default_lanes": 4, "default_maxspeed": 45 * mile / hour},
    "trunk_link": {"default_lanes": 4, "default_maxspeed": 45 * mile / hour},
    "primary": {"default_lanes": 4, "default_maxspeed": 45 * mile / hour},
    "primary_link": {"default_lanes": 4, "default_maxspeed": 45 * mile / hour},
    "secondary": {"default_lanes": 4, "default_maxspeed": 35 * mile / hour},
    "secondary_link": {"default_lanes": 4, "default_maxspeed": 35 * mile / hour},
    "tertiary": {"default_lanes": 2, "default_maxspeed": 30 * mile / hour},
    "tertiary_link": {"default_lanes": 2, "default_maxspeed": 30 * mile / hour},
    "unclassified": {"default_lanes": 2, "default_maxspeed": 25 * mile / hour},
    "residential": {"default_lanes": 2, "default_maxspeed": 25 * mile / hour},
}
