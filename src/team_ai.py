import random

from map import *

__all__ = [
    "generate_combination",
    "valid_entity",
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