from number_generator import RandomNumberGenerator
from typing import Tuple


def generate_knapsack(n: int) -> Tuple[list, list, int]:
    number_generator = RandomNumberGenerator(1234567890)
    capacity = number_generator.next_int(5 * n, 10 * n)
    costs = []
    weights = []
    for _ in range(n):
        costs.append(number_generator.next_int(1, 30))
        weights.append(number_generator.next_int(1, 30))

    return costs, weights, capacity
