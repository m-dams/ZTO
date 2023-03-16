from number_generator import RandomNumberGenerator
from instance import Instance


class Solution(Instance):
    def __init__(self, tasks_count):
        super().__init__(tasks_count)
        self.initialise()

    def print_result(self):
        for x in range(self.tasks_count):
            print("Task ", x)
            print("Execution time: ", self.execution_times[x])
            print("Deadline", self.deadlines[x])
            print("Weight", self.weights[x])
            print("Tardiness", self.tardiness[x], "\n")
        print("Order", self.order)
        print("Tardiness weighted and combined: ", self.tardiness_weighted)
        print("Schedule: ", self.task_complete_schedule)

    def print_score(self):
        print(self.tardiness_weighted)

    def calculate_tardiness(self):
        self.tardiness_weighted=0
        for x in range(self.tasks_count):
            curr_task_idx = self.order.index(x)
            self.tardiness[x] = self.task_complete_schedule[curr_task_idx] - self.deadlines[x]
            if self.tardiness[x] < 0:
                self.tardiness[x] = 0
            self.tardiness_weighted += self.tardiness[x] * self.weights[x]

    def calculate_schedule(self):
        for x in range(self.tasks_count):
            curr_task = self.order[x]
            if x > 0:
                self.task_complete_schedule.append(self.execution_times[curr_task] + self.task_complete_schedule[-1])
            else:
                self.task_complete_schedule.append(self.execution_times[curr_task])

    def initialise(self):
        number_generator = RandomNumberGenerator(1234567890)
        self.order = number_generator.rand_list(self.tasks_count)
        self.calculate_schedule()
        self.calculate_tardiness()

    def change_order(self, order):
        self.order = order
        self.calculate_schedule()
        self.calculate_tardiness()