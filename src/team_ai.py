import random
import copy

from map import *

__all__ = [
    "generate_combination",
    "valid_entity",
    "random_swap",
    "swap",
    "random_mutation",
    "mutate"
]

""" 
Modelagem do problema:
    O estado é representado por uma lista que contem sublistas representando cada um dos pokemons,
    nesse caso serão 5 sublistas.
    Cada sublista, que representa um pokemon, tem 6 elementos que representam as batalhas de ginasio
    na qual ele vai participar. 
    Heuristicas:
        - O pokemon mais fraco tem 5 elementos, já que é necessario que um pokemon esteja vivo no final
        - Todos os pokemons devem ser usados ao maximo
"""

# Entity = [[]]

POKEMON_N = 5
POKEMON_POWER = [1.5, 1.4, 1.3, 1.2, 1.1]
POKEMON_ENERGY = [6, 6, 6, 6, 5]

MAX_MUTATION_TRIES = 10

#class MutationError(Exception):
#    

def simulate():
    population = generate_initial_population(1000)

    
    
    return

def generate_initial_population(size : int) -> list:
    population = []
    for i in range(size):
        population.append(generate_combination())
    return population

def generate_combination() -> list:
    Entity = []
    gym_list = map_gym_list()
    
    free_pokemon = list(range(POKEMON_N))

    for _ in POKEMON_ENERGY:
        Entity.append([])

    for gym in gym_list:
        n = random.randint(0, len(free_pokemon)-1)
        index = free_pokemon[n]
        Entity[index].append(gym)
        if len(Entity[index]) >= POKEMON_ENERGY[index]:
            free_pokemon.pop(n)

    for index, pokemon in enumerate(Entity):
        while len(pokemon) < POKEMON_ENERGY[index]:
            gym = random.choice(gym_list)
            if gym not in pokemon:
                pokemon.append(gym)

    # for i, energy in enumerate(POKEMON_ENERGY):
    #     Entity.append([])
    #     for _ in range(energy):
    #         gym = random.choice(gym_list)
    #         Entity[i].append(gym)

    if valid_entity(Entity):
        return Entity
    
    return None
        
def valid_entity(entity : list):
    gym_list = map_gym_list()
    for pokemon in entity:
        for gym in pokemon:
            gym_count = pokemon.count(gym)
            if gym_count > 1:
                return False
            try:
                gym_list.remove(gym)
            except:
                continue

    return len(gym_list) == 0

def reproduce(entity : list):
    return

def random_swap(entity : list):

    availableIndex = list(range(len(entity)))
    pokemon_index = random.sample(availableIndex, k = 2)

    pokemon1 = entity[pokemon_index[0]]
    pokemon2 = entity[pokemon_index[1]]

    min_power = min(len(pokemon1), len(pokemon2))
    gym_index = random.randint(0, min_power - 1)

    return swap(entity, pokemon_index[0], pokemon_index[1], gym_index)

def swap(entity : list, pokemon_index_1 : int, pokemon_index_2 : int, gym_index : int) -> list:

    entity = copy.deepcopy(entity)

    pokemon_1 = entity[pokemon_index_1]
    pokemon_2 = entity[pokemon_index_2]

    gym_1 = pokemon_1[gym_index] 
    gym_2 = pokemon_2[gym_index] 

    if gym_1 in pokemon_2 or gym_2 in pokemon_1:
        raise Exception(f"Invalid swap (Repetead Pokemon in Gym): {pokemon_1}, {pokemon_2}, {gym_1}, {gym_2}")

    pokemon_1[gym_index] = gym_2
    pokemon_2[gym_index] = gym_1

    return entity

def random_mutation(entity : list):

    for _ in range(MAX_MUTATION_TRIES):
        pokemon_index = random.randint(0, len(entity) - 1)
        pokemon = entity[pokemon_index]
        gym_index = random.randint(0, len(pokemon) - 1)

        new_gym = random.choice(map_gym_list())
        while new_gym in pokemon:
            new_gym = random.choice(map_gym_list())

        try:
            mutated_pokemon = mutate(entity, pokemon_index, gym_index, new_gym)
            return mutated_pokemon
        except:
            continue

    raise Exception("Mutation Error: Reached max allowed mutation")

    

def mutate(entity : list, pokemon_index : int, gym_index : int, new_gym : str):

    entity = copy.deepcopy(entity)
    print(pokemon_index)
    pokemon = entity[pokemon_index]
    print(pokemon)
    gym = pokemon[gym_index]

    total_count = 0
    for poke in entity:
        total_count += poke.count(gym)

    if total_count <= 1:
        raise Exception(f"Invalid mutation (No Pokemon in Gym):\nPokemon: {pokemon}\nGym:{gym}")
    if new_gym in pokemon:
        raise Exception(f"Invalid mutation (Repeated Gym):\nPokemon: {pokemon}\nGym:{gym}")

    pokemon[gym_index] = new_gym

    print(entity)

    return entity