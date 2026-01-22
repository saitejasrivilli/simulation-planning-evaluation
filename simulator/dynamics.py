import numpy as np

def clip_velocity(velocity, max_speed):
    speed = np.linalg.norm(velocity)
    if speed > max_speed:
        return velocity / speed * max_speed
    return velocity


def integrate(position, velocity, dt):
    return position + velocity * dt
