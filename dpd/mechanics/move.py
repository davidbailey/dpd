def move(acceleration, initial_velocity, time, max_speed=None):
    final_velocity = initial_velocity + acceleration * time
    if max_speed is not None and final_velocity > max_speed:
        final_velocity = max_speed
        time_accelerating = (final_velocity - initial_velocity) / acceleration
        time_constant_speed = time - time_accelerating
        distance_accelerating = move(acceleration, initial_velocity, time_accelerating)[
            0
        ]
        distance_constant_speed = move(
            0 * acceleration, final_velocity, time_constant_speed
        )[
            0
        ]  # multiply 0 by accelration in case a units library (e.g. astropy.units) is used
        distance = distance_accelerating + distance_constant_speed
    else:
        distance = initial_velocity * time + 0.5 * acceleration * time**2
    return distance, final_velocity
