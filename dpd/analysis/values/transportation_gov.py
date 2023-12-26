from astropy import units
from pandas import Series

from dpd.analysis.units import person, usd2020

# https://www.transportation.gov/sites/dot.gov/files/2022-03/Benefit%20Cost%20Analysis%20Guidance%202022%20%28Revised%29.pdf

Value_of_Reduced_Fatalities_and_Injuries = Series(
    [
        3900 * usd2020,
        77200 * usd2020,
        151100 * usd2020,
        554800 * usd2020,
        11600000 * usd2020,
        210300 * usd2020,
        302600 * usd2020,
        12837400 * usd2020,
    ],
    index=[
        "O - No Injury",
        "C - Possible Injury",
        "B - Non-incapacitating",
        "A - Incapacitating",
        "K - Killed",
        "U - Injured (Severity Unknown)",
        "Injury Crash",
        "Fatal Crash",
    ],
    name="Value of Reduced Fatalities and Injuries",
)

Value_of_Travel_Time_Savings = Series(
    [
        16.20 * usd2020 / (person * units.hour),
        29.40 * usd2020 / (person * units.hour),
        17.80 * usd2020 / (person * units.hour),
        32.40 * usd2020 / (person * units.hour),
        32.00 * usd2020 / (person * units.hour),
        33.60 * usd2020 / (person * units.hour),
        50.70 * usd2020 / (person * units.hour),
        52.50 * usd2020 / (person * units.hour),
    ],
    index=[
        "General Travel Time - Personal",
        "General Travel Time - Business",
        "General Travel Time - All Purposes",
        "Walking Cycling, Waiting, Standing, and Transfer Time",
        "Commercial Vehicle Operators - Truck Drivers",
        "Commercial Vehicle Operators - Bus Drivers",
        "Commercial Vehicle Operators - Transit Rail Operators",
        "Commercial Vehicle Operators - Locomotive Engineers",
    ],
    name="Value of Travel Time Savings",
)
