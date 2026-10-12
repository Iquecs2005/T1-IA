import pytest

import string

from pokemon import *

@pytest.fixture(scope="function", autouse=True)
def init():
    pokemon_initial_state()

@pytest.fixture()
def gym_list():
    return string.ascii_lowercase

def test_pokemon_battle_power():
    no_pokemon = [False] * 5
    some_pokemon = [True, False, False, True, False]
    all_pokemon = [True] * 5

    assert pokemon_battle_power(no_pokemon) == 0
    assert pokemon_battle_power(some_pokemon) == 2.7
    assert pokemon_battle_power(all_pokemon) == 6.5

def test_pokemon_allocate(gym_list):
    pokemon_index = 0
    gym = gym_list[0]
    gym_index = 1

    # Ok allocation
    assert pokemon_current_energy(pokemon_index) == pokemon_max_energy(pokemon_index)
    assert pokemon_allocate(pokemon_index, gym)
    assert pokemon_current_energy(pokemon_index) == pokemon_max_energy(pokemon_index) - 1
    assert gym in pokemon_gym_list(pokemon_index) 

    # Repeated Allocation returns False
    with pytest.raises(PokemonAllocationError, match="Duplicated Gym"):
        pokemon_allocate(pokemon_index, gym)

    # Full pokemon allocation returns False
    pokemon_energy = pokemon_current_energy(pokemon_index)
    for _ in range(pokemon_energy):
        pokemon_allocate(pokemon_index, gym_list[gym_index])
        gym_index += 1

    assert pokemon_current_energy(pokemon_index) == 0

    with pytest.raises(PokemonAllocationError, match="Pokemon Unavailable"):
        assert pokemon_allocate(pokemon_index, gym_list[gym_index])

def test_pokemon_availability(gym_list):
    pokemon_index = 0
    gym_index = 0

    assert pokemon_current_energy(pokemon_index) == pokemon_max_energy(pokemon_index)
    assert pokemon_is_available(pokemon_index)
    assert pokemon_gym_list(pokemon_index) == []
    assert gym_index == 0

    while pokemon_is_available(pokemon_index):
        assert gym_list[gym_index] not in pokemon_gym_list(pokemon_index)
        assert pokemon_allocate(pokemon_index, gym_list[gym_index])
        assert gym_list[gym_index] in pokemon_gym_list(pokemon_index)
        gym_index += 1

    assert not pokemon_is_available(pokemon_index)
    assert gym_index == pokemon_max_energy(pokemon_index)

    with pytest.raises(PokemonAllocationError, match="Pokemon Unavailable"):
        assert pokemon_allocate(pokemon_index, gym_list[gym_index]) 

def test_all_pokemon_unavailable(gym_list):
    assert not all_pokemon_unavailable()

    for pokemon_index in range(pokemon_amount()):
        gym_index = 0
        for j in range(pokemon_max_energy(pokemon_index)):
            pokemon_allocate(pokemon_index, gym_list[gym_index])
            gym_index += 1

    assert all_pokemon_unavailable()

def test_get_random_available_pokemon(gym_list):

    pokemon_index = get_random_available_pokemon()

    assert pokemon_index is not None
    assert pokemon_current_energy(pokemon_index) > 0

    for pokemon_index in range(pokemon_amount()):
        gym_index = 0
        energy = pokemon_current_energy(pokemon_index)
        for j in range(energy):
            pokemon_allocate(pokemon_index, gym_list[gym_index])
            gym_index += 1

    assert all_pokemon_unavailable()

    with pytest.raises(PokemonAvailableError, match="No Available Pokemon"):
        get_random_available_pokemon()