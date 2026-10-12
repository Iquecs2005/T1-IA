import pytest

from team_ai import *
from map import *

# @pytest.fixture
# def base_entity():
#     entity = [['1', '2', '3'],
#               ['4', '5', '6']]
#     return entity

# @pytest.fixture
# def repeated_entity():
#     entity = [['1', '2', '3'],
#               ['1', '2', '3']]
#     return entity

# @pytest.fixture
# def assymetric_entity():
#     entity = [['1', '2', '3'],
#               ['4', '5', '6', '7']]
#     return entity

@pytest.fixture(scope="module", autouse=True)
def init():
    map_load("maps\\kanto.txt")

def test_new_entity():
    for _ in range(10):
        entity = new_entity()
        assert valid_entity(entity)
    pass

# def test_swap_ok(base_entity):
#     pokemon_index_1 = 0
#     pokemon_index_2 = 1
#     gym_index = 0

#     swaped_entity = swap(base_entity, pokemon_index_1, pokemon_index_2, gym_index)
    
#     assert swaped_entity != base_entity
#     assert swaped_entity[pokemon_index_1][gym_index] == base_entity[pokemon_index_2][gym_index]
#     assert swaped_entity[pokemon_index_2][gym_index] == base_entity[pokemon_index_1][gym_index]

# def test_swap_negative_index(base_entity):
#     pokemon_index_1 = -1
#     pokemon_index_2 = -2
#     gym_index = -1
    
#     swaped_entity = swap(base_entity, pokemon_index_1, pokemon_index_2, gym_index)
        
#     assert swaped_entity != base_entity
#     assert swaped_entity[pokemon_index_1][gym_index] == base_entity[pokemon_index_2][gym_index]
#     assert swaped_entity[pokemon_index_2][gym_index] == base_entity[pokemon_index_1][gym_index]

# def test_swap_assymetric_ok(assymetric_entity):
#     pokemon_index_1 = 0
#     pokemon_index_2 = 1
#     gym_index = 0

#     swaped_entity = swap(assymetric_entity, pokemon_index_1, pokemon_index_2, gym_index)
            
#     assert swaped_entity != assymetric_entity
#     assert swaped_entity[pokemon_index_1][gym_index] == assymetric_entity[pokemon_index_2][gym_index]
#     assert swaped_entity[pokemon_index_2][gym_index] == assymetric_entity[pokemon_index_1][gym_index]

# def test_swap_invalid_index(base_entity):
#     pokemon_index_1 = 0
#     pokemon_index_2 = 1
#     impossible_pokemon_index = len(base_entity)
#     gym_index = 0
#     impossible_gym_index_1 = len(base_entity[pokemon_index_1])
#     impossible_gym_index_2 = len(base_entity[pokemon_index_2])

#     with pytest.raises(IndexError):
#         swap(base_entity, pokemon_index_1, impossible_pokemon_index, gym_index)
#     with pytest.raises(IndexError):
#         swap(base_entity, impossible_pokemon_index, pokemon_index_2, gym_index)
#     with pytest.raises(IndexError):
#         swap(base_entity, pokemon_index_1, pokemon_index_2, impossible_gym_index_1)
#     with pytest.raises(IndexError):
#         swap(base_entity, pokemon_index_1, pokemon_index_2, impossible_gym_index_2)

# def test_swap_assymetric_uneven_acess(assymetric_entity):
#     pokemon_index_1 = 0
#     pokemon_index_2 = 1
#     gym_index = len(assymetric_entity[pokemon_index_2]) - 1 

#     with pytest.raises(IndexError):
#         swap(assymetric_entity, pokemon_index_1, pokemon_index_2, gym_index)

# def test_swap_impossible(repeated_entity):
#     pokemon_index_1 = 0
#     pokemon_index_2 = 1
#     gym_index = 0

#     with pytest.raises(Exception):
#         swap(repeated_entity, pokemon_index_1, pokemon_index_2, gym_index)

# def test_random_swap(base_entity):
#     for i in range(10):
#         swaped_entity = random_swap(base_entity)
#         assert swaped_entity != base_entity

# def test_mutation_ok(repeated_entity):
#     pokemon_index = 0
#     gym_index = 0
#     new_gym = '4'

#     mutated_entity = mutate(repeated_entity, pokemon_index, gym_index, new_gym)

#     assert mutated_entity != repeated_entity
#     assert mutated_entity[pokemon_index][gym_index] == new_gym

# def test_mutation_impossible(base_entity, repeated_entity):
#     pokemon_index = 0
#     gym_index = 0
#     new_gym = '4'

#     with pytest.raises(Exception):
#         mutate(base_entity, pokemon_index, gym_index, new_gym)
    
#     pokemon_index = 0
#     gym_index = 0
#     new_gym = '2'

#     with pytest.raises(Exception):
#         mutate(repeated_entity, pokemon_index, gym_index, new_gym)