from solution import Solution
import random as rd


def get_fitness(solution):
    return solution.tardiness_weighted


def generate_weights(operator):
    result = []
    for i in range(1, operator + 1):
        result.append(i)
    return result[::-1]


def roulette_probability_substract_from_max(parents):
    weights = []
    max_fitness = 0
    for x in parents:
        if max_fitness < x.tardiness_weighted:
            max_fitness = x.tardiness_weighted

    for x in parents:
        weights.append((max_fitness - x.tardiness_weighted) if x.tardiness_weighted > 0 else weights.append(max_fitness))
    return weights


def roulette_probability_division(parents):
    weights = []
    for x in parents:
        weights.append(round(1/x.tardiness_weighted, 10) if x.tardiness_weighted > 0 else weights.append(0))
    return weights


class Generation:
    def __init__(self, solutions, crossover_chance, mutation_chance, tournament_operator, population, tasks_count):
        self.solutions = solutions
        self.crossover_chance = crossover_chance
        self.mutation_chance = mutation_chance
        self.tournament_operator = tournament_operator
        self.population = population
        self.next_generation = []
        self.tasks_count = tasks_count

    def tournament(self):
        new_generation = []
        elite = round(self.population / 10)
        # elite = round(self.population / 1000000)
        elite_members = sorted(self.solutions, key=get_fitness)

        for x in range(elite):
            new_generation.append(elite_members[0])
            elite_members.pop(0)

        for x in range(self.population - elite):
            parents = rd.choices(self.solutions, k=self.tournament_operator)
            parents = sorted(parents, key=get_fitness)
            new_generation.append(parents[0])
        self.next_generation = new_generation

    # Alternative version of tournament combined with roulette probability
    # def tournament(self):
    #     new_generation = []
    #     for x in range(self.population):
    #         parents = rd.choices(self.solutions, k = self.tournament_operator)
    #         parents = sorted(parents, key=self.get_fitness, reverse=True)
    #         parent = rd.choices(parents, weights=self.generate_weights(self.tournament_operator), k = 1)
    #         new_generation.append(parent[0])
    #     self.next_generation = new_generation

    def roulette(self):
        new_generation = []
        for x in range(self.population):
            parents = sorted(self.solutions, key=get_fitness)
            parent = rd.choices(parents, weights=roulette_probability_division(parents), k=1)
            new_generation.append(parent[0])
        self.next_generation = new_generation

    def pm_crossover(self):
        pass

    def ox_crossover(self):
        new_generation = []
        cross_chance = self.crossover_chance * 100

        for x in range(self.population):
            chance = rd.randint(1, 100)
            if cross_chance >= chance:
                parent1 = rd.choices(self.next_generation, k=1)
                parent2 = rd.choices(self.next_generation, k=1)
                order1 = parent1[0].order
                order2 = parent2[0].order
                child_genotype = [-1] * self.tasks_count
                start, end = sorted(rd.randrange(self.tasks_count) for _ in range(2))
                child_inherited = []
                for i in range(start, end + 1):
                    child_genotype[i] = order1[i]
                    child_inherited.append(order1[i])

                current_parent_position = 0

                fixed_pos = list(range(start, end + 1))
                i = 0
                while i < self.tasks_count:
                    if i in fixed_pos:
                        i += 1
                        continue

                    test_child = child_genotype[i]
                    if test_child == -1:
                        parent_trait = order2[current_parent_position]
                        while parent_trait in child_inherited:
                            current_parent_position += 1
                            parent_trait = order2[current_parent_position]
                        child_genotype[i] = parent_trait
                        child_inherited.append(parent_trait)
                    i += 1
                # print(child_genotype)

                child = Solution(self.tasks_count)
                child.change_order(child_genotype)
                new_generation.append(child)
            else:
                child = rd.choices(self.next_generation, k=1)
                new_generation.append(child[0])
        self.next_generation = new_generation

    def mutation_ox(self):
        mut_chance = self.mutation_chance * 100
        for n in range(len(self.next_generation)):
            chance = rd.randint(1, 100)
            if mut_chance >= chance:
                parent1 = self.next_generation[n]
                parent2 = Solution(self.tasks_count)
                order1 = parent1.order
                order2 = parent2.order
                mutant_genotype = [-1] * self.tasks_count
                start, end = sorted(rd.randrange(self.tasks_count) for _ in range(2))
                mutant_inherited = []
                for i in range(start, end + 1):
                    mutant_genotype[i] = order1[i]
                    mutant_inherited.append(order1[i])

                current_parent_position = 0
                fixed_pos = list(range(start, end + 1))
                i = 0
                while i < self.tasks_count:
                    if i in fixed_pos:
                        i += 1
                        continue

                    test_mutant = mutant_genotype[i]
                    if test_mutant == -1:
                        parent_trait = order2[current_parent_position]
                        while parent_trait in mutant_inherited:
                            current_parent_position += 1
                            parent_trait = order2[current_parent_position]
                        mutant_genotype[i] = parent_trait
                        mutant_inherited.append(parent_trait)
                    i += 1

                mutant = Solution(self.tasks_count)
                mutant.change_order(mutant_genotype)
                self.next_generation[n] = mutant

    def mutation(self):
        mut_chance = self.mutation_chance * 100
        for n in range(len(self.next_generation)):
            chance = rd.randint(1, 100)
            if mut_chance >= chance:
                self.next_generation[n] = Solution(self.tasks_count)

    def particle_swarm_optimization(self):
        for x in self.next_generation:
            if x.tardiness_weighted < x.personal_best:
                x.personal_best = x.tardiness_weighted
                x.personal_best_order = x.order

    def create_offspring(self):
        self.tournament()
        # self.roulette()
        self.ox_crossover()
        # self.mutation()
        self.mutation_ox()
        self.particle_swarm_optimization()

        return self.next_generation
