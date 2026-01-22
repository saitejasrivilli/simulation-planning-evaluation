import numpy as np

def noisy_observation(x, noise_std):
    if noise_std <= 0:
        return x
    return x + np.random.normal(0.0, noise_std, size=x.shape)
