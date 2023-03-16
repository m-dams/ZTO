import math
import random


class RandomNumberGenerator:
    def __init__(self, seed=None):
        self.__seed = seed

    def next_int(self, low, high) -> int:
        m = 2147483647
        a = 16807
        b = 127773
        c = 2836
        k = int(self.__seed / b)
        self.__seed = a * (self.__seed % b) - k * c
        if self.__seed < 0:
            self.__seed = self.__seed + m
        value_0_1 = self.__seed
        value_0_1 = value_0_1 / m

        return low + int(math.floor(value_0_1 * (high - low + 1)))

    def next_float(self, low, high) -> float:
        low *= 100000
        high *= 100000
        val = self.next_int(low, high) / 100000.0

        return val

    @staticmethod
    def rand_list(tasks_count):
        return random.sample(range(0, tasks_count), tasks_count)

