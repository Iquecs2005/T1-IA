import random
import math
import copy

from pokemon import *
from gym import *

__all__ = [
    "new_entity",
    "valid_entity",
    "print_entity",
    "simulate",
    "_single_swap",
    "_double_swap",
    "_swap",
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

# Entity = [[]]

def new_entity() -> dict[list]:
    pokemon_initial_state()
    gym_list = get_gym_list()

    entity : dict[list] = dict()
    for gym in gym_list:
        entity[gym] = []
        for _ in range(pokemon_amount()):
            entity[gym].append(False)

    # Choose at least one pokemon for each gym 
    for gym in gym_list:
        free_pokemon = get_random_available_pokemon()
        entity[gym][free_pokemon] = True
        pokemon_allocate(free_pokemon, gym)

    # Add pokemon until all are unavailable
    while not all_pokemon_unavailable():
        gym = random.choice(gym_list)
        free_pokemon = get_random_available_pokemon()
        if not entity[gym][free_pokemon]:
            entity[gym][free_pokemon] = True
            pokemon_allocate(free_pokemon, gym)

    if valid_entity(entity):
        return entity
    
    return None
        
def valid_entity(entity : dict[list]) -> bool:
    gym_list = get_gym_list()

    if len(entity) != len(gym_list):
        return False
    
    pokemon_count = []
    for _ in range(pokemon_amount()):
        pokemon_count.append(0)

    for gym in entity:
        if gym not in gym_list:
            return False
        
        pokemon_list = entity[gym]

        if pokemon_list.count(True) == 0:
            return False

        for index, value in enumerate(pokemon_list):
            if value:
                pokemon_count[index] += 1

    for pokemon_index, pokemon_count in enumerate(pokemon_count):
        if pokemon_max_energy(pokemon_index) != pokemon_count:
            return False

    return True

def print_entity(entity : dict[list]) -> None:
    for gym in entity:
        print(f"{gym}:  ", end = "")
        
        pokemon_list = entity[gym]
        
        print("%-5s" % str(pokemon_list[0]), end = "")
        for value in pokemon_list[1:]:
            print("   %-5s" % str(value), end="")
        print()

    return

def simulate(initial_population_size : int,
             max_generations : int,
             children_per_generation : int,
             new_elements_per_generation : int,
             entity_lifespan : int,
             no_improvement_max : int) -> tuple[dict, float]:
    
    population = _generate_population(initial_population_size)
    minimum_entity = []
    minimum_time = math.inf
    no_improvement = 0

    for _ in range(max_generations):
        _age_population(population)

        minimum_entity, current_minimum_time = _min_time(population, minimum_entity, minimum_time)
        # TODO Research if this is the correct aproach
        if minimum_time - current_minimum_time < 0.1:
            no_improvement += 1
            if no_improvement >= no_improvement_max:
                return minimum_entity, current_minimum_time
        else:
            no_improvement = 0

        minimum_time = current_minimum_time

        parents = _select_parents(population, children_per_generation)
        children = _reproduce(parents)
        young_population = _remove_oldest(population, entity_lifespan)
        new_entities = _generate_population(new_elements_per_generation)

        population = young_population
        population.extend(children)
        population.extend(new_entities)

    return minimum_entity, minimum_time

def _generate_population(size : int) -> list[list[dict, int]]:
    population = []
    for _ in range(size):
        population.append([new_entity(), 0])
    return population

def _age_population(population : list[list[dict, int]]) -> list[list[dict, int]]:
    index = 0
    for i in population:
        index += 1
        i[1] += 1

    return population

def _min_time(population : list[list[dict, int]], minimum_entity : dict[list], minimum_time : float) -> tuple[dict, float]:
    for entity in population:
        total_time = _fitness_function(entity[0])
        if total_time < minimum_time:
            minimum_time = total_time
            minimum_entity = entity[0].copy()
    
    return minimum_entity, minimum_time

def _fitness_function(entity : dict[list]) -> float:
    total_time = 0

    for gym in entity:
        pokemon_list = entity[gym]
        power = pokemon_battle_power(pokemon_list)
        total_time += gym_battle_time(gym, power)

    return total_time

def _total_fitness(population : list[list[dict, int]]) -> float:
    total_time = 0

    for entity in population:
        total_time += 1 / _fitness_function(entity[0])
    
    return total_time

def _select_parent(population : list[list[dict, int]], total_fitness : float):
    n = random.uniform(0, 1)
    current_amount = 0

    for entity in population:
        prob = (1 / _fitness_function(entity[0])) / total_fitness
        current_amount += prob
        if n < current_amount:
            return entity[0]

def _select_parents(population, amount : int) -> list[dict]:
    parents = []
    total_fitness = _total_fitness(population)
    for _ in range(amount):
        parents.append(_select_parent(population, total_fitness))
    return parents

def _reproduce(parents : list[dict]) -> list[list[dict, int]]:
    children = []
    for entity in parents:
        swap_amounts = random.randint(1, 10)
        child_entity = copy.deepcopy(entity)
        for i in range(swap_amounts):
            child_entity = _random_swap(child_entity)
        children.append([child_entity, 0])
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

def _remove_oldest(population, entity_lifespan):
    young_population = []
    for entity in population:
        if entity[1] < entity_lifespan:
            young_population.append(entity)
    return young_population