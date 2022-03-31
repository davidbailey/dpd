from pandas import Series
from .currency import Currency

usd = Currency("USD", 2020, 0.07).discount()

# https://www.transportation.gov/sites/dot.gov/files/2022-03/Benefit%20Cost%20Analysis%20Guidance%202022%20%28Revised%29.pdf

Value_of_Reduced_Fatalties_and_Injuries = Series(
    [3900 * usd, 77200 * usd, 151100 * usd, 554800 * usd, 11600000 * usd, 210300 * usd, 302600 * usd, 12837400 * usd],
    index=[
        "O - No Injury",
        "C - Possible Injury",
        "B - Non-incapacitating",
        "A - Incapacitating",
        "k - Killed",
        "U - Injured (Severity Unknown)",
        "Injury Crash",
        "Fatal Crash",
    ],
    name="Value of Reduced Fatalties and Injuries"
)
