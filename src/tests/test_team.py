from gym import *
from pokemon import *
from team import *

def test_new_team():
    gym_list = ['a', 'b']
    team = new_team(gym_list)
    poke_amount = pokemon_amount()

    for gym, pokemon_list in team.items():
        assert gym in gym_list
        assert len(pokemon_list) == poke_amount
        for pokemon in pokemon_list:
            assert not pokemon

def test_valid_team():
    gym_list = ['a', 'b', 'c', 'd', 'e', 'f']

    valid = {'a': [True, True, True, True, True],
             'b': [True, True, True, True, True],
             'c': [True, True, True, True, True],
             'd': [True, True, True, True, True],
             'e': [True, True, True, True, True],
             'f': [True, True, True, True, False]}
    
    assert valid_team(valid, gym_list)
    
    repeated_gym = {'a': [True, True, True, True, True],
                 'b': [True, True, True, True, True],
                 'c': [True, True, True, True, True],
                 'd': [True, True, True, True, True],
                 'a': [True, True, True, True, True],
                 'f': [True, True, True, True, False]}
    
    assert not valid_team(repeated_gym, gym_list)

    not_enough_elements = {'a': [True, True, True, True, True],
                           'b': [True, True, True, True, True],}
    
    assert not valid_team(not_enough_elements, gym_list)

    incorrect_gym_list = ['a', 'b', 'a', 'b', 'a', 'b']

    assert not valid_team(valid, incorrect_gym_list)

def test_new_random_team():
    gym_list = get_gym_list()

    for i in range(1000):
        team = new_random_team(gym_list)
        assert valid_team(team, gym_list)

def test_team_battle_time():
    team = {'2': [True, True, True, True, True],
            '3': [True, False, False, False, False],
            '4': [False, False, False, False, True]}

    assert team_battle_time(team, '2') == gym_battle_time('2', 6.5)
    assert team_battle_time(team, '3') == gym_battle_time('3', 1.5)
    assert team_battle_time(team, '4') == gym_battle_time('4', 1.1)

def test_team_total_battle_time():
    team = {'2': [True, True, True, True, True],
            '3': [True, False, False, False, False],
            '4': [False, False, False, False, True]}

    total = 0

    for gym, pokemon_list in team.items():
        total += gym_battle_time(gym, pokemon_battle_power(pokemon_list))

    assert total == team_total_battle_time(team)