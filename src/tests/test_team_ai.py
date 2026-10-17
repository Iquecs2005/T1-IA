import pytest
from unittest.mock import patch

from team_ai import *
from team_ai import _calculate_prob, _total_fitness, _fitness_function, _select_parent

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

@pytest.fixture()
def basic_population():
    return [[{'2': [True, False, False, True, False]}, 0],
            [{'2': [True, True, False, False, False]}, 0]]

def test_fitness_function(basic_population):
    entity_1 = basic_population[0][0]
    entity_2 = basic_population[1][0]

    entity_1_fitness = 1 / (35 / (1.5 + 1.2))
    entity_2_fitness = 1 / (35 / (1.5 + 1.4))

    assert _fitness_function(entity_1) == entity_1_fitness
    assert _fitness_function(entity_2) == entity_2_fitness

def test_total_fitness(basic_population):
    entity_1 = basic_population[0][0]
    entity_2 = basic_population[1][0]

    entity_1_fitness = _fitness_function(entity_1)
    entity_2_fitness = _fitness_function(entity_2)

    total = entity_1_fitness + entity_2_fitness

    assert _total_fitness(basic_population) == total

def test_calculate_prob(basic_population):
    entity_1 = basic_population[0][0]
    entity_2 = basic_population[1][0]

    entity_1_fitness = _fitness_function(entity_1)
    entity_2_fitness = _fitness_function(entity_2)

    total = _total_fitness(basic_population)

    prob_1 = _calculate_prob(entity_1, total)
    prob_2 = _calculate_prob(entity_2, total)

    mock_prob_1 = entity_1_fitness / total
    mock_prob_2 = entity_2_fitness / total

    assert prob_1 == mock_prob_1
    assert prob_2 == mock_prob_2
    assert pytest.approx(prob_1 + prob_2) == 1

def test_select_parent(basic_population):
    total = _total_fitness(basic_population)
    prob = _calculate_prob(basic_population[0][0], total)
    
    with patch('random.uniform') as mock_uniform:
        mock_uniform.return_value = prob - 0.01
        
        parent = _select_parent(basic_population, total)

        mock_uniform.assert_called_once()
        assert parent == basic_population[0][0]

    with patch('random.uniform') as mock_uniform:
        mock_uniform.return_value = prob + 0.01

        parent = _select_parent(basic_population, total)

        mock_uniform.assert_called_once()
        assert parent == basic_population[1][0]