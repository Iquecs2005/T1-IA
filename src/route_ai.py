import random
import copy
from gym import get_gym_list

__all__ = [
    "set_gym_amount",
    "set_distances",
    "new_entity",
    "valid_entity",
    "print_entity",
    "simulate_route",
]


def set_gym_amount(value: int):
    global gym_amount

    gym_amount = value


def set_distances(distances_matrix: list[list]):
    global distances

    distances = distances_matrix


def new_entity() -> list:
    entity = get_gym_list()
    random.shuffle(entity)
    return entity


def valid_entity(entity: list):
    if len(entity) != gym_amount:
        return False
    expected = get_gym_list()
    return sorted(entity) == expected


def print_entity(entity: list):
    print("1", end="")
    for i in entity:
        print(f" -> {i}", end="")
    print(" -> U")


def simulate_route(initial_population_size: int,
             max_generations: int,
             children_per_generation: int,
             new_elements_per_generation: int,
             entity_lifespan: int,
             no_improvement_max: int) -> tuple[list, int]:

    population = _generate_population(initial_population_size, 0)

    minimum_entity = population[0][0]
    minimum_cost = _fitness_function(population[0][0])

    last_improvement = 0

    for generation in range(max_generations):
        minimum_entity, current_minimum_cost, improved = _min_cost(population, minimum_entity, minimum_cost)

        if improved:
            last_improvement = generation
        else:
            if _early_stop(generation, last_improvement, no_improvement_max):
                break

        minimum_cost = current_minimum_cost

        parents = _select_parents(population, children_per_generation)
        children = _reproduce(parents, generation)
        young_population = _remove_oldest(population, entity_lifespan, generation)
        new_entities = _generate_population(new_elements_per_generation, generation)

        population = young_population
        population.extend(children)
        population.extend(new_entities)

    return minimum_entity, 1 / minimum_cost


def _generate_population(size: int, generation : int) -> list[list[list, int]]:
    population = []
    for _ in range(size):
        population.append([new_entity(), generation])
    return population


def _min_cost(population: list[list[list, int]], minimum_entity: list, minimum_cost: int) -> tuple[list, int]:
    improved = False

    for entity in population:
        cost = _fitness_function(entity[0])
        if cost > minimum_cost:
            minimum_cost = cost
            minimum_entity = entity[0].copy()
            improved = True

    return minimum_entity, minimum_cost, improved


def _early_stop(current_gen : int, last_improvement : int, no_improvement_max : int) -> bool:
    if current_gen - last_improvement >= no_improvement_max:
        return True
    return False


def _fitness_function(entity: list) -> int:
    total_cost = 0
    current = 0

    gym_order = get_gym_list()

    for i in entity:
        gym_index = gym_order.index(i) + 1
        total_cost += distances[current][gym_index]
        current = gym_index

    total_cost += distances[current][gym_amount + 1]

    return 1 / total_cost


def _total_fitness(population: list[list[list, int]]) -> int:
    total_cost = 0
    for entity in population:
        total_cost += _fitness_function(entity[0])

    return total_cost


def _calculate_prob(entity, total):
    return _fitness_function(entity) / total


def _select_parent(population: list[list[list, int]], total_fitness: int):
    n = random.uniform(0, 1)
    current_amount = 0

    for entity in population:
        prob = _calculate_prob(entity[0], total_fitness)
        current_amount += prob
        if n < current_amount:
            return entity[0]


def _select_parents(population: list[list, int], amount: int) -> list[list]:
    parents = []
    total_fitness = _total_fitness(population)
    for _ in range(amount):
        parents.append(_select_parent(population, total_fitness))
    return parents


def _reproduce(parents: list[list], generation) -> list[list[list, int]]:
    children = []
    for entity in parents:
        swap_amounts = random.randint(1, 10)
        child_entity = copy.deepcopy(entity)
        for i in range(swap_amounts):
            child_entity = _random_swap(child_entity)
        children.append([child_entity, generation])
    return children


def _random_swap(entity: list) -> list:
    if random.choice([True, False]):
        return _single_swap(entity)
    else:
        return _double_swap(entity)


def _single_swap(entity: list) -> list:
    i, j = random.sample(range(len(entity)), 2)
    entity[i], entity[j] = (entity[j], entity[i])

    return entity


def _double_swap(entity: list) -> list:
    i, j = sorted(random.sample(range(len(entity)), 2))
    entity[i:j+1] = reversed(entity[i:j+1])

    return entity


def _remove_oldest(population: list[list, int], entity_lifespan: int, generation : int) -> list[list, int]:
    young_population = []
    for entity in population:
        if generation - entity[1] < entity_lifespan:
            young_population.append(entity)
    return young_population
