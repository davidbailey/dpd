def step(acceleration, initial_velocity, time, max_speed=None):
    final_velocity = initial_velocity + acceleration * time
    if max_speed and final_velocity > max_speed:
        final_velocity = max_speed
        time_accelerating = (final_velocity - initial_velocity) / acceleration
        time_constant_speed = time - time_accelerating
        distance_accelerating = step(acceleration, inital_velocity, time_accelerating)[
            0
        ]
        distance_constant_speed = step(0, final_velocity, time_constant_speed)[0]
        distance = distance_accelerating + distance_constant_speed
    else:
        distance = initial_velocity * time + 0.5 * acceleration * time ** 2
    return distance, final_velocity
