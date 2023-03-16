from solution import Solution
import time
from generation import Generation


def get_fitness(solution):
    return solution.tardiness_weighted


def generate_initial_population(tasks_count, population):
    initial = []
    for x in range(2000):
        initial.append(Solution(tasks_count))
    temp = sorted(initial, key=get_fitness)
    for x in range(round(population/5)):
        initial.append(temp[x])
    for x in range(population - round(population/5)):
        initial.append(Solution(tasks_count))
    return initial


def main():
    start_time = time.time()

    # main parameters
    tasks_count = 30
    step_interval = 0.00
    population = 100
    crossover_chance = 0.7
    mutation_chance = 0.05
    tournament_operator = 3
    num_of_generations = 100
    generations = []
    best_specimens = []

    for _ in range(num_of_generations):
        generations.append(Generation([], crossover_chance, mutation_chance, tournament_operator,
                                      population, tasks_count))

    generations[0].solutions = generate_initial_population(tasks_count, population)

    generations[0].solutions[0].print_result()
    best_solution = generations[0].solutions[0]
    for s in generations[0].solutions:
        if s.tardiness_weighted < best_solution.tardiness_weighted:
            best_solution = s

    fitness_difference = 0

    print(f'{best_solution.tardiness_weighted}')
    all_time_best = best_solution
    best_specimens.append(best_solution.tardiness_weighted)

    i = 0
    while i < num_of_generations - 1:
        generations[i + 1].solutions = generations[i].create_offspring()
        best_solution = generations[i + 1].solutions[0]
        past_all_best = all_time_best.tardiness_weighted
        for s in generations[i + 1].solutions:
            if s.tardiness_weighted < best_solution.tardiness_weighted:
                best_solution = s

            if s.tardiness_weighted < all_time_best.tardiness_weighted:
                all_time_best = s
            if past_all_best > all_time_best.tardiness_weighted:
                fitness_difference = past_all_best - all_time_best.tardiness_weighted
            else:
                fitness_difference = 0

        # print(f'{best_solution.tardiness_weighted}')
        if fitness_difference != 0:
            print(f'Gen {i} {all_time_best.tardiness_weighted}')

        best_specimens.append(best_solution.tardiness_weighted)
        i += 1
        time.sleep(step_interval)  # for better visibility

    print('All time best:')
    # all_time_best.print_score()
    print("--- %s seconds ---" % (time.time() - start_time))


def fitness_of_solutions(index, generations):
    print(" - END - ")
    for s in generations[0].solutions:
        print(s.tardiness_weighted)
    print('---------------------------')
    for s in generations[index].solutions:
        print(s.tardiness_weighted)


if __name__ == "__main__":
    main()
