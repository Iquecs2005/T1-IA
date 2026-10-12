import pytest

from gym import *

def test_get_gym_list():
    gym_list = get_gym_list()

    assert gym_list[0] == '2'
    assert gym_list[14] == 'I'
    assert gym_list[23] == 'T'

def test_gym_battle_time():
    assert gym_battle_time('2', 1) == 35
    assert gym_battle_time('7', 1.5) == 40
    assert gym_battle_time('P', 4) == 40