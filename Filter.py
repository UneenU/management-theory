import numpy as np
from collections import deque
from math import *

class NoiseFilter:
    def __init__(self, window_size=20):
        self.window_size = window_size
        self.buffer = deque(maxlen=window_size)
        # Инициализируем буфер нулями
        for _ in range(window_size):
            self.buffer.append(0.0)

    def filter(self, input_value):
        """
        Фильтрует помехи из входного значения
        Не знает о реализации генератора помех
        """
        # Добавляем новое значение в буфер
        self.buffer.append(input_value)

        # Создаем копию буфера для обработки
        buffer = list(self.buffer)

        # Медианная фильтрация для удаления выбросов
        median = np.median(buffer)

        # Вычисляем порог для определения выбросов
        threshold = self._calculate_threshold(buffer, median)

        # Заменяем выбросы на медианное значение
        filtered_buffer = []
        for value in buffer:
            if abs(value - median) > threshold:
                filtered_buffer.append(median)
            else:
                filtered_buffer.append(value)

        # Применяем скользящее среднее
        smoothed_value = np.mean(filtered_buffer)

        return smoothed_value

    def _calculate_threshold(self, data, median):
        """Вычисляет порог для определения выбросов"""
        # Вычисляем среднеквадратичное отклонение
        deviations = [abs(x - median) for x in data]
        std_dev = np.std(deviations) if deviations else 0

        # Порог в 2 стандартных отклонения
        return 2.0 * std_dev if std_dev > 0 else 1.0

    def set_window_size(self, new_size):
        """Изменение размера окна фильтра"""
        self.window_size = new_size
        current_data = list(self.buffer)
        self.buffer = deque(maxlen=new_size)
        # Сохраняем последние данные или заполняем нулями
        for value in current_data[-new_size:]:
            self.buffer.append(value)
        # Дополняем нулями если нужно
        while len(self.buffer) < new_size:
            self.buffer.append(0.0)


class KalmanFilter:
    def __init__(self):
        self.squared_sigma_etta = 0.005 ** 2
        self.expected_squared_e = self.squared_sigma_etta
        self.squared_sigma_ksi = self.squared_sigma_etta
        self.x_opt = 0

    def __call__(self, position, u):
        K = (self.expected_squared_e + self.squared_sigma_ksi) / (
                self.expected_squared_e + self.squared_sigma_ksi + self.squared_sigma_etta)
        self.expected_squared_e = K * self.squared_sigma_etta
        self.squared_sigma_ksi = self.expected_squared_e / 4
        self.x_opt = K * position + (1-K) * (self.x_opt + u)
        return self.x_opt