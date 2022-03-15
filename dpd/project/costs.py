from astropy import units
from forex_python.converter import CurrencyRates

USD = units.def_unit(["USD"])
eur_usd = CurrencyRates().get_rates("EUR")["USD"]
EUR = units.def_unit(["EUR"], eur_usd * USD)

elevations = {
    "surface": {"dollars_per_meter": 1000},
    "underground": {"dollars_per_meter": 2000},
    "elevated": {"dollars_per_meter": 1500},
}

modes = ["air", "marine", "rail", "road"]


def segment_cost(mode, elevation, length):
    pass
