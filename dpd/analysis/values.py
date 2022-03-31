from pandas import Series
from .currency import Currency

usd = Currency("USD", 2020, 0.07)

# https://www.transportation.gov/sites/dot.gov/files/2022-03/Benefit%20Cost%20Analysis%20Guidance%202022%20%28Revised%29.pdf

Value_of_Reduced_Fatalties_and_Injuries = Series(
    [3900, 77200, 151100, 554800, 11600000, 210300, 302600, 12837400],
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
)
