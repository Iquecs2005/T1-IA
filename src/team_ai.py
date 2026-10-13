import random
import copy

from pokemon import *
from gym import *
from team import *

__all__ = [
    "simulate",
]

""" 
Modelagem do problema:
    O estado é representado por um dicionario onde as chaves são os ginasios e o conteudo é uma lista
    de tamanho igual ao numero total de pokemons, onde cada elemento é True ou False dependendo se o
    pokemon com aquele indice irá lutar naquele ginasio.
    Heuristicas:
        - O pokemon mais fraco tem 5 elementos, já que é necessario que um pokemon esteja vivo no final
        - Todos os pokemons devem ser usados ao maximo
"""

def simulate(initial_population_size : int,
             max_generations : int,
             children_per_generation : int,
             new_elements_per_generation : int,
             entity_lifespan : int,
             no_improvement_max : int) -> tuple[dict, float]:

    gym_list = get_gym_list()
    population = _generate_population(initial_population_size, 0, gym_list)

    best_team = population[0][0]
    best_fit = _fitness_function(population[0][0])
    
    last_improvement = 0

    for generation in range(1, max_generations):
        best_team, best_fit, improved = _best_team(population, best_team, best_fit)

        if improved:
            last_improvement = generation
        else:
            if _early_stop(generation, last_improvement, no_improvement_max):
                break

        parents = _select_parents(population, children_per_generation)
        children = _reproduce(parents, generation)
        young_population = _remove_oldest(population, entity_lifespan, generation)
        new_entities = _generate_population(new_elements_per_generation, generation, gym_list)

        population = young_population
        population.extend(children)
        population.extend(new_entities)

    return best_team, 1 / best_fit

def _generate_population(size : int, generation : int, gym_list : list[str]) -> list[list[dict, int]]:
    population = []
    for _ in range(size):
        population.append([new_random_team(gym_list), generation])
    return population

def _best_team(population : list[list[dict, int]], best_team : dict[list], best_fit : float) -> tuple[dict, float, bool]:
    improved = False
    
    for team in population:
        fitness_value = _fitness_function(team[0])
        if fitness_value < best_fit:
            best_fit = fitness_value
            best_team = team[0].copy()
            improved = True
    
    return best_team, best_fit, improved

def _early_stop(current_gen : int, last_improvement : int, no_improvement_max : int) -> bool:
    if current_gen - last_improvement >= no_improvement_max:
        return True
    return False

def _fitness_function(team : dict[list]) -> float:
    return 1 / team_total_battle_time(team)

def _total_fitness(population : list[list[dict, int]]) -> float:
    total_time = 0

    for team in population:
        total_time += _fitness_function(team[0])
    
    return total_time

def _calculate_prob(entity, total):
    return _fitness_function(entity) / total

def _select_parent(population : list[list[dict, int]], total_fitness : float):
    n = random.uniform(0, 1)
    current_amount = 0

    for entity in population:
        prob = _calculate_prob(entity[0], total_fitness)
        current_amount += prob
        if n < current_amount:
            return entity[0]

def _select_parents(population, amount : int) -> list[dict]:
    parents = []
    total_fitness = _total_fitness(population)
    for _ in range(amount):
        parents.append(_select_parent(population, total_fitness))
    return parents

def _reproduce(parents : list[dict], generation) -> list[list[dict, int]]:
    children = []
    for entity in parents:
        swap_amounts = random.randint(1, 10)
        child_entity = copy.deepcopy(entity)
        for i in range(swap_amounts):
            child_entity = _random_swap(child_entity)
        children.append([child_entity, generation])
    return children

def _random_swap(entity : dict[list]) -> dict[list]:
    if random.choice([True, False]):
        return _single_swap(entity)
    else:
        return _double_swap(entity)

def _single_swap(entity : dict):
    keys = list(entity.keys())
    gym_1 = None

    while keys != []:
        gym_1 = random.choice(keys)

        selected_gym : list = entity[gym_1]

        true_index = []
        true_amount = 0
        for index, pokemon in enumerate(selected_gym):
            if pokemon:
                true_index.append(index)
                true_amount += 1

        if true_amount > 1:
            break
        elif true_amount < 1:
            raise Exception()

        keys.remove(gym_1)
    else:
        raise Exception()

    pokemon_index = random.choice(true_index)
    keys = list(entity.keys())
    keys.remove(gym_1)
    gym_2 = random.choice(keys)

    return _swap(entity, gym_1, gym_2, pokemon_index)

def _double_swap(entity : dict):
    gyms = random.sample(list(entity.keys()), k = 2)

    selected_gyms = [entity[gyms[0]], entity[gyms[1]]]

    entity[gyms[0]] = selected_gyms[1]
    entity[gyms[1]] = selected_gyms[0]

    return entity

def _swap(entity : dict[list], gym_1 : str, gym_2 : str, pokemon_index : int) -> dict[list]:
    value_1 = entity[gym_1][pokemon_index]
    value_2 = entity[gym_2][pokemon_index]

    entity[gym_1][pokemon_index] = value_2
    entity[gym_2][pokemon_index] = value_1

    return entity

def _remove_oldest(population, entity_lifespan, generation):
    young_population = []
    for entity in population:
        if generation - entity[1] < entity_lifespan:
            young_population.append(entity)
    return young_population