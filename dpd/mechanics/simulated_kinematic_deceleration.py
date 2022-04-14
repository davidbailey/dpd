class SimulatedKinematicDeceleration:
    """
    Provides methods to decelerate the body with constant deceleration.
    """

    def __init__(
        self,
        max_deceleration,
    ):
        self.max_deceleration = max_deceleration

    def stopping_distance(self, final_velocity):
        return (final_velocity**2 - self.current_velocity**2) / (
            2 * self.max_deceleration
        )

    def decelerate(self, distance, final_velocity):
        self.current_time += 2 * distance / (final_velocity + self.current_velocity)
        self.current_distance += distance
        self.current_velocity = final_velocity
        return self.current_time, self.current_distance
