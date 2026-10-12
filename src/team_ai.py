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
    "_swap"
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
             parents_per_generation : int,
             entity_lifespan : int) -> tuple[dict, float]:
    
    population = _generate_initial_population(initial_population_size)
    minimum_entity = []
    minimum_time = math.inf

    for _ in range(max_generations):
        _age_population(population)

        minimum_entity, minimum_time = _min_time(population, minimum_entity, minimum_time)

        parents = _select_parents(population, parents_per_generation)
        children = _reproduce(parents)
        young_population = _remove_oldest(population, entity_lifespan)

        population = young_population
        population.extend(children)

    return minimum_entity, minimum_time

def _generate_initial_population(size : int) -> list[list[dict, int]]:
    population = []
    for _ in range(size):
        population.append([new_entity(), 0])
    return population

def _age_population(population : list[list[dict, int]]) -> list[list[dict, int]]:
    for i in population:
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
        total_time += _fitness_function(entity[0])
    
    return total_time

def _select_parent(population : list[list[dict, int]], total_fitness : float):
    n = random.uniform(0, 1)
    current_amount = 0

    for entity in population:
        prob = _fitness_function(entity[0]) / total_fitness
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
        children.append([_swap(entity), 0])
    return children

def _swap(entity : dict[list]) -> dict[list]:
    child_entity = copy.deepcopy(entity)
    keys = list(entity.keys())
    gym = None

    while keys != []:
        gym = random.choice(keys)
        keys.remove(gym)

        selected_gym : list = entity[gym]

        pokemon_in_gym = selected_gym.count(True)
        if pokemon_in_gym < 1:
            raise Exception()
        elif pokemon_in_gym > 1:
            break
    else:
        raise Exception()

    possible_index = list(range(len(selected_gym)))
    index = None

    while possible_index != []:
        index = random.choice(possible_index)
        possible_index.remove(index)
        if selected_gym[index]:
            break
    else:
        raise Exception()

    keys = list(entity.keys())
    keys.remove(gym)

    while keys != []:
        second_gym = random.choice(keys)
        keys.remove(second_gym)

        if not entity[second_gym][index]:
            child_entity[gym][index] = False
            child_entity[second_gym][index] = True
            break
    else:
        raise Exception()

    return child_entity

def _remove_oldest(population, entity_lifespan):
    young_population = []
    for entity in population:
        if entity[1] < entity_lifespan:
            young_population.append(entity)
    return young_population