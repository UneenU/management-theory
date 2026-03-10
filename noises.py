import numpy as np
import random


class NoiseGenerator:
    def __init__(self, intensity=0.005):
        self.noise_intensity = intensity
        self.rng = np.random.default_rng()

    def add_noise(self, input_value):
        """
        Добавляет помехи к входному значению
        """
        # Гауссовский шум
        noise = self.rng.normal(0, self.noise_intensity)
        # С вероятностью 5% добавляем импульсную помеху
        # if random.random() < 0.05:
        #     impulse_noise = self.rng.normal(0, self.noise_intensity * 10)
        #     noise += impulse_noise

        return input_value + noise

    def set_intensity(self, intensity):
        """Установка интенсивности помех"""
        self.noise_intensity = intensity
