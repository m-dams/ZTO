from number_generator import RandomNumberGenerator
from typing import Tuple


def generate_tasks(n: int) -> Tuple[list, list, list]:
    number_generator = RandomNumberGenerator(1234567)
    execution_times = []
    deadlines = []
    weights = []
    exec_time_combined = 0

    for _ in range(n):
        execution_times.append(number_generator.next_int(1, n))
        weights.append(number_generator.next_int(1, n))
        exec_time_combined += execution_times[-1]
    for _ in range(n):
        deadlines.append(number_generator.next_int(1, exec_time_combined))
    return execution_times, weights, deadlines


class Instance:
    def __init__(self, tasks_count):
        self.tasks_count = tasks_count
        self.execution_times, self.weights, self.deadlines = generate_tasks(tasks_count)
        self.order = []
        self.tardiness = [0] * self.tasks_count
        self.tardiness_weighted = 0
        self.task_complete_schedule = []
        self.personal_best = 1000000
        self.personal_best_order = []
