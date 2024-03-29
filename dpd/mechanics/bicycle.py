from numpy import cos, sin, tan


class Bicycle:
    """
    A bicycle model. References:
    * https://thomasfermi.github.io/Algorithms-for-Automated-Driving/Control/BicycleModel.html
    * https://arrow.tudublin.ie/cgi/viewcontent.cgi?article=1002&context=engschmecart
    """

    def __init__(self, x, y, theta, velocity, vehicle_length):
        self.x = x
        self.y = y
        self.theta = theta
        self.velocity = velocity
        self.vehicle_length = vehicle_length

    def step(self, delta_time=1, steering_angle=0):
        self.x = self.x + self.velocity * cos(self.theta) * delta_time
        self.y = self.y + self.velocity * sin(self.theta) * delta_time
        self.theta = (
            self.theta
            + self.velocity * tan(steering_angle) / self.vehicle_length * delta_time
        )

    def get_radius_from_vehicle_length_and_steering_angle(self, steering_angle):
        return self.vehicle_length / tan(steering_angle)
