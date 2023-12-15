from astropy import units
from pandas import Series

from dpd.analysis.units import usd

units.imperial.enable()

# https://i.redd.it/foothill-gold-line-project-in-la-county-has-finished-the-v0-vzmva9y0718b1.jpg?s=6ab75401465331a038c6e20c34cff18f82729313
# https://foothillgoldline.org/wp-content/uploads/2023/06/Quarter2_Newsletter_Spring2023_FINAL_Online.pdf

LightRail = Series(
    [
        2 * units.imperial.mile / units.imperial.mile,
        2110 / units.imperial.mile,
        2110 * 4 / units.imperial.mile,
        121000 * units.imperial.pounds / units.imperial.mile,
        38 / units.imperial.mile,
    ],
    index=[
        "Rail Miles / Mile",
        "Railroad Ties / Mile",
        "Rail Clips / Mile",
        "Pounds of Ballast / Mile",
        "OCS Poles / Mile",
    ],
    name="Light Rail",
)

# https://twitter.com/numble/status/1671948453528891392

HeavyRail = Series(
    [
        2 * units.imperial.mile / units.imperial.mile,
        4214 * usd / units.imperial.foot,
    ],
    index=[
        "Rail Miles / Mile",
        "Cost / Mile (Unpowered, at-grade)",
    ],
    name="Heavy Rail",
)
