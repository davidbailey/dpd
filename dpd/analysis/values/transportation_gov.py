from astropy import units
from pandas import Series
from dpd.analysis.units import person, usd

# https://www.transportation.gov/sites/dot.gov/files/2022-03/Benefit%20Cost%20Analysis%20Guidance%202022%20%28Revised%29.pdf

Value_of_Reduced_Fatalities_and_Injuries = Series(
    [
        3900 * usd,
        77200 * usd,
        151100 * usd,
        554800 * usd,
        11600000 * usd,
        210300 * usd,
        302600 * usd,
        12837400 * usd,
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
        16.20 * usd / (person * units.hour),
        29.40 * usd / (person * units.hour),
        17.80 * usd / (person * units.hour),
        32.40 * usd / (person * units.hour),
        32.00 * usd / (person * units.hour),
        33.60 * usd / (person * units.hour),
        50.70 * usd / (person * units.hour),
        52.50 * usd / (person * units.hour),
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
