from number_generator import RandomNumberGenerator
from docplex.mp.model import Model


if __name__ == "__main__":
    number_generator = RandomNumberGenerator(1234567890)
    executors_count = number_generator.next_int(9, 20)
    tasks_count = executors_count
    cost = [[number_generator.next_int(1, 50) for _ in range(tasks_count)] for _ in range(executors_count)]

    model = Model(name='zagadnienie_przydzialu')
    solution = []
    for i in range(executors_count):
        solution.append([model.integer_var(lb=0, ub=1, name=f"x[{i},{j}]") for j in range(tasks_count)])
    model.minimize(model.sum(solution[e][t]*cost[e][t] for e in range(executors_count) for t in range(tasks_count)))
    # constraints
    for e in range(executors_count):
        model.add_constraint(model.sum(solution[e][t] for t in range(tasks_count)) == 1)
        model.add_constraint(model.sum(solution[t][e] for t in range(tasks_count)) == 1)
    model.solve(log_output=True)
    # model.print_solution()
