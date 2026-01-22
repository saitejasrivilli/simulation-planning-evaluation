class VehicleModel:
    def __init__(self, max_speed=1.0):
        self.max_speed = max_speed

    def enforce_limits(self, velocity):
        speed = (velocity[0]**2 + velocity[1]**2) ** 0.5
        if speed > self.max_speed:
            return velocity / speed * self.max_speed
        return velocity
