from __future__ import annotations
from itertools import count
from typing import Optional, Tuple
from math import ceil

from number_generator import RandomNumberGenerator
import numpy as np
from queue import PriorityQueue, Queue
from pydot import Node, Edge, Dot


class Matrix:
    def __init__(self):
        self.distances = np.zeros((5, 5))

    @property
    def n(self):
        return self.distances.shape[0]

    def reduce(self) -> int:
        row_reduction = self.__reduce_rows()
        column_reduction = self.__reduce_columns()

        return row_reduction + column_reduction

    def mark_as_visited(self, row: int, column: int) -> None:
        for i in range(self.n):
            self.distances[row][i] = -1
            self.distances[i][column] = -1
        self.distances[column][row] = -1

    def copy(self) -> 'Matrix':
        clone = Matrix()
        clone.distances = np.copy(self.distances)

        return clone

    def __reduce_rows(self) -> int:
        reduction = 0
        for i in range(self.n):
            row = self.distances[i, :]
            min_distance = find_min_distance(row)
            if min_distance != -1:
                subtract_from_distances(row, min_distance)
                reduction += min_distance

        return reduction

    def __reduce_columns(self) -> int:
        reduction = 0
        for j in range(self.n):
            column = self.distances[:, j]
            min_distance = find_min_distance(column)
            if min_distance != -1:
                subtract_from_distances(column, min_distance)
                reduction += min_distance

        return reduction


class Route:
    def __init__(self):
        self.cities = []
        self.__cost = 0

    def print(self):
        print(" --> ".join(map(str, self.cities)))

    def cost(self, matrix: Matrix):
        if self.__cost == 0:
            for i in range(len(self.cities) - 1):
                self.__cost += matrix.distances[self.cities[i]][self.cities[i+1]]

        return self.__cost

    def last_city(self) -> int:
        return self.cities[-1]

    def copy(self) -> 'Route':
        route_copy = Route()
        route_copy.cities = self.cities.copy()

        return route_copy

    def end_cycle(self) -> None:
        self.cities.append(self.cities[0])


class City:
    def __init__(self, name: int, matrix: Matrix):
        self.name = name
        self.matrix = matrix
        self.root = None
        self.children = []
        self.route = Route()
        self.route.cities.append(self.name)
        self.lower_bound = None
        self.cut_off = False

    def add(self, city: 'City') -> None:
        city.root = self
        city.route = self.route.copy()
        city.route.cities.append(city.name)
        self.children.append(city)


def calculate_node(node: City) -> None:
    city_from = node.route.last_city()
    for city_to in range(node.matrix.n):
        if node.matrix.distances[city_from][city_to] != -1 and city_to != 0:
            city = City(city_to, node.matrix.copy())
            node.add(city)
            travel_cost = node.matrix.distances[city_from][city_to]
            city.matrix.mark_as_visited(city_from, city_to)
            city.lower_bound = node.lower_bound + city.matrix.reduce() + travel_cost


class BNB:
    def __init__(self, matrix: Optional[Matrix]):
        self.matrix = matrix if matrix is not None else random_matrix()
        self.upper_bound, self.root = heuristic_solution(self.matrix.copy())

    def solve(self) -> Route:
        queue = PriorityQueue()
        unique = count()
        queue_push(queue, unique, self.root)

        while not queue.empty():
            parent = queue.get()[2]

            if len(parent.children) == 0:
                calculate_node(parent)

            for child in parent.children:
                if child.lower_bound <= self.upper_bound:
                    queue_push(queue, unique, child)
                else:
                    child.cut_off = True

        if len(parent.route.cities) == self.matrix.n:
            parent.route.end_cycle()

        return parent.route


class BS:
    def __init__(self, matrix: Optional[Matrix]):
        self.matrix = matrix if matrix is not None else random_matrix()
        self.upper_bound, self.root = heuristic_solution(self.matrix.copy())
        self.k = .7

    def solve(self) -> Route:
        queue = PriorityQueue()
        unique = count()
        queue_push(queue, unique, self.root)

        while not queue.empty():
            parent = queue.get()[2]

            if len(parent.children) == 0:
                calculate_node(parent)

            child_count = ceil(self.k * len(parent.children))
            for child in parent.children:
                if child.lower_bound <= self.upper_bound and child_count > 0:
                    queue_push(queue, unique, child)
                    child_count -= 1
                else:
                    child.cut_off = True

        if len(parent.route.cities) == self.matrix.n:
            parent.route.end_cycle()

        return parent.route


def random_matrix(n: int = 5) -> Matrix:
    number_generator = RandomNumberGenerator(1234567890)
    matrix = Matrix()
    matrix.distances = np.array([
            [number_generator.next_int(1, 30) if i != j else -1 for j in range(n)]
            for i in range(n)
        ], np.int32)

    return matrix


def plot_tree(root: City, name: str) -> None:
    graph = Dot(graph_type='digraph')
    roots = Queue()
    roots.put(root)
    counter = 0

    while not roots.empty():
        root = roots.get()
        # painting
        root_id = str(counter) + str(root.name)
        root_node = Node(root_id, label=root.name)
        graph.add_node(root_node)
        for child in root.children:
            child_id = str(counter+1) + str(child.name)
            if child.cut_off:
                node = Node(child_id, label=child.name, style="filled", fillcolor="red")
            else:
                node = Node(child_id, label=child.name)
                roots.put(child)
            graph.add_node(node)
            graph.add_edge(Edge(root_id, child_id))
        counter += 1

    graph.write_png(name + ".png")


def queue_push(queue: PriorityQueue, unique, node: City) -> None:
    queue.put((node.lower_bound, next(unique), node))


def can_visit(cost: int):
    return cost != 0 and cost != -1


def find_min_distance(distances: []) -> int:
    found_min = distances[0]
    for distance in distances[1:]:
        if (distance < found_min and distance != -1) or found_min == -1:
            found_min = distance

    return found_min


def subtract_from_distances(costs: np.array, subtrahend: int) -> None:
    for i in range(len(costs)):
        if can_visit(costs[i]):
            costs[i] -= subtrahend


def heuristic_solution(matrix: Matrix) -> Tuple[int, City]:
    upper_bound = 0
    queue = PriorityQueue()
    root = City(0, matrix.copy())
    root.lower_bound = root.matrix.reduce()
    unique = count()
    queue_push(queue, unique, root)

    while not queue.empty():
        node = queue.get()[2]
        if len(node.route.cities) == matrix.n:
            node.route.end_cycle()
            upper_bound = node.lower_bound
        calculate_node(node)
        if len(node.children) > 0:
            min_bound = node.children[0].lower_bound
            min_child = node.children[0]
            for child in node.children[1:]:
                if child.lower_bound < min_bound:
                    min_bound = child.lower_bound
                    min_child = child
            queue_push(queue, unique, min_child)

    return upper_bound, root


matrix = random_matrix(7)
tsp = BNB(matrix)
route = tsp.solve()
route.print()
print(route.cost(matrix))
plot_tree(tsp.root, "szkoda_ze_nie_5")
