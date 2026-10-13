import random

from pokemon import *
from gym import *

__all__ = [
    "new_team",
    "valid_team",
    "new_random_team",
    "print_team",
    "team_battle_time",
    "team_total_battle_time",
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

def new_team(gym_list : list[str]) -> dict[list]:
    poke_amount = pokemon_amount()

    team : dict[list] = dict()
    for gym in gym_list:
        team[gym] = [False] * poke_amount
    
    return team

def valid_team(team : dict[list], gym_list : list[str]) -> bool:
    gym_list = gym_list.copy()

    if len(team) != len(gym_list):
        return False
    
    pokemon_count = [0] * pokemon_amount()

    for gym, pokemon_list in team.items():
        if gym not in gym_list:
            return False

        gym_list.remove(gym)

        valid = False
        for index, value in enumerate(pokemon_list):
            if value:
                pokemon_count[index] += 1
                valid = True

        if not valid:
            return False

    for pokemon_index, pokemon_count in enumerate(pokemon_count):
        if pokemon_max_energy(pokemon_index) != pokemon_count:
            return False

    return True

def new_random_team(gym_list : list[str]) -> dict[list]:
    pokemon_initial_state()

    team = new_team(gym_list)

    # Choose at least one pokemon for each gym 
    for gym, pokemon_list in team.items():
        free_pokemon = get_random_available_pokemon()
        pokemon_list[free_pokemon] = True
        pokemon_allocate(free_pokemon, gym)

    # Add pokemon until all are unavailable
    while not all_pokemon_unavailable():
        gym = random.choice(gym_list)
        free_pokemon = get_random_available_pokemon()
        if not team[gym][free_pokemon]:
            team[gym][free_pokemon] = True
            pokemon_allocate(free_pokemon, gym)
    
    return team

def print_team(team : dict[list]) -> None:

    energy_count = []
    for i in range(pokemon_amount()):
        energy_count.append(pokemon_max_energy(i))

    energy_count[-1] += 1

    for gym, pokemon_list in team.items():
        print(f"{gym}:  ", end = "")

        first_value = True
        for i, value in enumerate(pokemon_list):
            if not value:
                continue

            energy_count[i] -= 1

            if first_value:
                print(f"{pokemon_name(i)}", end="")
                first_value = False
            else:
                print(f", {pokemon_name(i)}", end="")
        print()

    print()
    print("Energia:")
    print()

    for i, energy in enumerate(energy_count):
        print(f"{pokemon_name(i)}: \t{energy} / {pokemon_max_energy(0)}")

    print()

    return

def team_battle_time(team : dict[list], gym: str) -> float:
    pokemon_list = team[gym]
    power = pokemon_battle_power(pokemon_list)
    time = gym_battle_time(gym, power)

    return time

def team_total_battle_time(team : dict[list]) -> float:
    total = 0
    
    for gym in team:
        total += team_battle_time(team, gym)

    return total