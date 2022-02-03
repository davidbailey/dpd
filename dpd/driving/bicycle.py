import math


class Bicycle: 
    """
    A bicycle model. References:
    * https://thomasfermi.github.io/Algorithms-for-Automated-Driving/Control/BicycleModel.html
    * https://arrow.tudublin.ie/cgi/viewcontent.cgi?article=1002&context=engschmecart
    """
    def __init__(self, x, y, theta, velocity, acceleration, vehicle_length):
        self.x = x
        self.y = y
        self.theta = theta
        self.velocity = velocity
        self.acceleration = acceleration
        self.vehicle_length = vehicle_length
    def step(self, delta_time=1, steering_angle=0):
        self.x = self.x + self.velocity * math.cos(self.theta) * delta_time
        self.y = self.y + self.velocity * math.sin(self.theta) * delta_time
        self.theta = self.theta + self.velocity * math.tan(steering_angle)/self.vehicle_length * delta_time
        self.velocity = self.velocity + self.acceleration * delta_time
    def get_radius_from_vehicle_length_and_steering_angle(self, steering_angle):
        return self.vehicle_length / math.tan(steering_angle)


truck = Bicycle(x=0, y=0, theta=0, velocity=1, acceleration=0, vehicle_length=29.5) # feet
truck.get_radius_from_vehicle_length_and_steering_angle(steering_angle=.61) # radians ~ 35 degrees
# 42.20804673074035 feet
