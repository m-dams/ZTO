from number_generator import RandomNumberGenerator
from collections import defaultdict
from docplex.mp.model import Model


if __name__ == "__main__":
    number_generator = RandomNumberGenerator(1234)
    tasks_count = number_generator.next_int(9, 20)
    machines_count = number_generator.next_int(1, 9)
    total_speed = number_generator.next_float(machines_count, 2 * machines_count)
    tasks_data = [(number_generator.next_float(1, 20), number_generator.next_int(0, machines_count - 1)) for _ in range(tasks_count)]
    # tasks_data = [(pi, ai), ...]

    model = Model(name='problem_szeregowania_ciagly')
    machines_speed = []
    for m in range(machines_count):
        machines_speed.append(model.continuous_var(lb=0.1, ub=total_speed, name=f"m{m}_speed"))
    actual_tasks_time = []
    for i in range(tasks_count):
        actual_tasks_time.append((tasks_data[i][0] * machines_speed[tasks_data[i][1]], tasks_data[i][1]))
        # actual_tasks_time = [(actual_time_for_task, ai), ...]
    machines_work_time = defaultdict(int)
    for at in actual_tasks_time:
        machines_work_time[at[1]] += at[0]
    max_machine = model.continuous_var(name="max_machine")
    model.minimize(max_machine)
    # constraint
    for machine_time in machines_work_time:
        model.add_constraint(max_machine >= machines_work_time[machine_time])
    for m in range(machines_count):
        model.add_constraint(machines_speed[m] >= 0.1)
    model.add_constraint(model.sum(machines_speed[m] for m in range(machines_count)) == total_speed)
    model.solve(log_output=True)
    model.print_solution()
