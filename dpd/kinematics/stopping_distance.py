def stopping_distance(deceleration, initial_velocity, final_velocity):
    distance = (final_velocity ** 2 - initial_velocity ** 2) / (2 * deceleration)
    return distance
