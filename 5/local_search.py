import math
from random import randint, random
from typing import Tuple
from abc import ABC, abstractmethod
from stop_conditions import StopCondition
from knapsack import generate_knapsack


class LocalSearch(ABC):
    def __init__(self, items_count: int, stop_condition: StopCondition):
        self.items_count = items_count
        self._solution = [False] * self.items_count
        self.worths, self.weights, self.capacity = generate_knapsack(items_count)
        self._stop_condition = stop_condition

    def _is_correct(self, solution: list) -> bool:
        weight = 0
        for item in range(self.items_count):
            if solution[item]:
                weight += self.weights[item]

        return weight <= self.capacity

    def _is_better(self, solution1: list, solution2: list) -> bool:
        worth1, _ = self._knapsack_value(solution1)
        worth2, _ = self._knapsack_value(solution2)

        return worth1 > worth2

    def _knapsack_value(self, solution) -> Tuple[int, int]:
        worth = 0
        weight = 0
        for item in range(self.items_count):
            if solution[item]:
                worth += self.worths[item]
                weight += self.weights[item]

        return worth, weight

    def _print_solution(self) -> None:
        worth, weight = self._knapsack_value(self._solution)

        print(f"Waga plecaka: {self.capacity}, waga uzyskana: {weight}, wartość: {worth}")
        print(f"Koszty: {self.worths}")
        print(f"Wagi: {self.weights}")
        print(f"Rozwiązanie: {self._solution}")

    def generate_random_solution(self, n_iter: int) -> None:
        solution = [False] * self.items_count
        for _ in range(n_iter):
            new_solution = self.move(solution)
            if self._is_correct(new_solution) and self._is_better(new_solution, solution):
                solution = new_solution

        self._solution = solution

    def move(self, solution) -> list:
        item = randint(0, self.items_count - 1)
        new_solution = solution.copy()
        new_solution[item] = not self._solution[item]

        return new_solution

    @abstractmethod
    def solve(self) -> None:
        raise NotImplemented


class RS(LocalSearch):
    def solve(self) -> None:
        while not self._stop_condition.should_stop():
            new_solution = self.move(self._solution)
            if not self._is_correct(new_solution):
                self._stop_condition.set_improvement(False)
            elif self._is_better(new_solution, self._solution):
                self._stop_condition.set_improvement(True)
                self._solution = new_solution
            else:
                self._stop_condition.set_improvement(False)
        self._print_solution()


class Cooling(ABC):
    def __init__(self, delta_t):
        self._delta_t = delta_t

    @abstractmethod
    def cool_down(self, temperature) -> float:
        raise NotImplemented


class GeometricCooling(Cooling):
    def cool_down(self, temperature) -> float:
        return self._delta_t * temperature


class LinearCooling(Cooling):
    def cool_down(self, temperature) -> float:
        temp = temperature - self._delta_t
        if temp <= 0:
            temp = 0.001

        return temp


class SA(LocalSearch):
    def __init__(self, items_count, stop_condition: StopCondition, cooling: Cooling):
        super().__init__(items_count, stop_condition)
        self.__cooling = cooling
        self.__temperature = self.__calculate_start_temperature(1000)

    def __calculate_start_temperature(self, n_iter: int) -> int:
        solution = self.move([False] * self.items_count)
        min_value, _ = self._knapsack_value(solution)
        max_value = 0
        for _ in range(n_iter):
            new_solution = self.move(solution)
            if self._is_correct(new_solution):
                value, _ = self._knapsack_value(new_solution)
                if value >= max_value:
                    max_value = value
                if value < min_value:
                    min_value = value

        return max_value - min_value

    def __cool_down(self) -> None:
        self.__temperature = self.__cooling.cool_down(self.__temperature)

    def __calculate_probability(self, new_solution: list) -> float:
        current_worth, _ = self._knapsack_value(self._solution)
        new_worth, _ = self._knapsack_value(new_solution)

        try:
            probability = math.exp(-(new_worth - current_worth) / self.__temperature)
        except OverflowError:
            probability = 0

        return probability

    def __should_accept_solution(self, new_solution: list) -> bool:
        probability = self.__calculate_probability(new_solution)

        return random() <= probability

    def solve(self):
        while not self._stop_condition.should_stop():
            new_solution = self.move(self._solution)
            if not self._is_correct(new_solution):
                self._stop_condition.set_improvement(False)
            elif self._is_better(new_solution, self._solution) or self.__should_accept_solution(new_solution):
                self._stop_condition.set_improvement(True)
                self._solution = new_solution
            else:
                self._stop_condition.set_improvement(False)
            self.__cool_down()
        self._print_solution()

