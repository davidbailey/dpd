from datetime import datetime

from astropy import units
from forex_python.converter import CurrencyRates

class Currency:
    def __init__(self, currency, base_year, discount_rate, base_currency=None):
        """
        Args:
            currency (str): e.g. USD, EUR
            base_year (int): e.g. 2020
            discount_rate (float): e.g. 0.07
            base_currency (astropy.units.quantity.Quantity): e.g. dpd.analysis.Currency.discount()
        """
        if base_currency:
            exchange_rate = CurrencyRates().get_rate(currency, base_currency.unit.name, datetime(year=base_year, month=1, day=1))
            self.currency = units.def_unit([currency], exchange_rate * base_currency)
        else:
            self.currency = units.def_unit([currency])
        self.base_year = base_year
        self.discount_rate = discount_rate
        self.base_currency = base_currency

    def discount(self, year=None):
        """
        Args:
            year (int): e.g. 2023
        Returns:
            currency (astropy.units.quantity.Quantity): a unit that can be multiplied by a value. e.g. 100 * Currency.discount()
        """
        if year is None:
            year = self.base_year
        return self.currency / ((1 + self.discount_rate) ** (year - self.base_year))
