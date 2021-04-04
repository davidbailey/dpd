def step(acceleration, initial_velocity, time):
    distance = initial_velocity * time + .5 * acceleration * time ** 2
    final_velocity = initial_velocity + acceleration * time
    return distance, final_velocity
