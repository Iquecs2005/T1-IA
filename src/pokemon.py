import random

__all__ = [
    "PokemonAllocationError",
    "PokemonAvailableError",

    "pokemon_amount",
    "pokemon_name",
    "pokemon_power",
    "pokemon_max_energy",
    "pokemon_current_energy",
    "pokemon_gym_list",
    "pokemon_battle_power",
    "pokemon_is_available",
    "get_random_available_pokemon",
    "all_pokemon_unavailable",
    "pokemon_allocate",
    "pokemon_initial_state",
]

AMOUNT = 5
NAME = ["Pikachu", "Bulbassauro", "Rattata", "Caterpie", "Weedle"]
POWER = [1.5, 1.4, 1.3, 1.2, 1.1]
# Heuristicas: O pokemon mais fraco tem 5 elementos, já que é necessario que um pokemon esteja vivo no final
MAX_ENERGY = [6, 6, 6, 6, 5]

current_energy = []
gym_list = []

# ============================================
#               Exceptions
# ============================================

class PokemonAllocationError(Exception):
    def __init__(self, error):
        super().__init__(error)
        self.error = error


class PokemonAvailableError(Exception):
    def __init__(self, error):
        super().__init__(error)
        self.error = error

# ============================================
#                Functions
# ============================================

def pokemon_amount() -> int:
    return AMOUNT


def pokemon_name(index : int) -> str:
    return NAME[index]


def pokemon_power(index : int) -> int:
    return POWER[index]


def pokemon_max_energy(index : int) -> int:
    return MAX_ENERGY[index]


def pokemon_current_energy(index : int) -> int:
    return current_energy[index]


def pokemon_gym_list(index : int) -> list:
    return gym_list[index].copy()


def pokemon_battle_power(pokemon : list) -> float:
    battle_power = 0
    
    for index, value in enumerate(pokemon):
        if value:
            battle_power += POWER[index]

    return battle_power


def pokemon_is_available(index : int) -> bool:
    return current_energy[index] > 0


def get_random_available_pokemon() -> int:
    if all_pokemon_unavailable():
        raise PokemonAvailableError("No Available Pokemon")

    available_pokemon = []
    for i in range(AMOUNT):
        if pokemon_is_available(i):
            available_pokemon.append(i)

    if available_pokemon == []:
        raise PokemonAvailableError("No Available Pokemon")

    random_index = random.randint(0, len(available_pokemon) - 1)
    return available_pokemon[random_index]


def all_pokemon_unavailable() -> bool:
    for i in range(AMOUNT):
        if pokemon_is_available(i):
            return False
    return True


def pokemon_allocate(index : int, gym : chr) -> bool:
    if not pokemon_is_available(index):
        raise PokemonAllocationError(error = "Pokemon Unavailable")
    if gym in gym_list[index]:
        raise PokemonAllocationError(error = "Duplicated Gym")

    current_energy[index] -= 1
    gym_list[index].append(gym)

    return True


def pokemon_initial_state() -> None:
    global current_energy, gym_list

    current_energy = MAX_ENERGY[:]
    gym_list = []
    for i in range(AMOUNT):
        gym_list.append([])


pokemon_initial_state()