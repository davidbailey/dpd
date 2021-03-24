def dms_to_dd(coordinate):
    """
    coordinate: '40°48′31″N'
    """
    degrees, remainder = coordinate.split("°")
    if "′" in remainder:
        minutes, remainder = remainder.split("′")
        if "″" in remainder:
            seconds, remainder = remainder.split("″")
        else:
            seconds = 0
    else:
        minutes = 0
        seconds = 0
    decimal_degrees = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if remainder == "E" or remainder == 'N':
        decimal_degrees *= -1
    return decimal_degrees
