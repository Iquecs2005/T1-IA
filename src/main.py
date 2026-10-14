from map import *
from team import *
from team_ai import *
from route_ai import *
from pathfinding import generate_distances_matrix, get_route

def main():
    # map_load("maps\\kanto.txt")
    # map_print()
    # print(map_rows())
    # print(map_collumn())
    # print(map_tile_value((-1, -1)))
    # print(map_start_pos())
    # print(map_tile_value((23, 35)))
    # print(map_end_pos())
    # print(map_tile_value((1, 16)))
    # print(map_gym_list())
    # print(map_gym_list())
    # print(map_find_gym("8"))
    # print(map_tile_value((14,117)))
    # print(map_get_neighbors_pos((-1,-1)))
    # print(generate_combination())
    # print(valid_entity([map_gym_list()[:5],map_gym_list()[5:]]))
    # print(valid_entity([['3'],['3']]))
    # print(valid_entity([['3','3']]))

    # entity = new_entity()
    # print_entity(entity)
    # print()
    # child = _single_swap(entity)
    # print()
    # print_entity(child)

    #for i in range(2):
    # entity, time = simulate(initial_population_size = 1000,
    #                         max_generations = 1000,
    #                         children_per_generation = 500,
    #                         new_elements_per_generation = 500,
    #                         entity_lifespan = 3,
    #                         no_improvement_max = 30)

    # initial_population_size = 1000
    # max_generations = 1000
    # children_per_generation = 500
    # new_elements_per_generation = 500
    # entity_lifespan = 3
    # no_improvement_max = 30
    map_load("maps/Kanto.txt")

    initial_population_size = 1000
    max_generations = 500
    children_per_generation = 500
    new_elements_per_generation = 500
    entity_lifespan = 5
    no_improvement_max = 20

    team, time = simulate(initial_population_size,
                            max_generations,
                            children_per_generation,
                            new_elements_per_generation,
                            entity_lifespan,
                            no_improvement_max)

    print(f"Tempo Total batalhas = {time}\n")
    print(f"Time encontrado:\n")
    print_team(team)

    set_gym_amount(24)
    set_distances(generate_distances_matrix(get_map(), map_start_pos(), map_end_pos()))

    initial_population_size = 1000
    max_generations = 1000
    children_per_generation = 500
    new_elements_per_generation = 100
    entity_lifespan = 5
    no_improvement_max = 50

    route, cost = simulate_route(initial_population_size,
                            max_generations,
                            children_per_generation,
                            new_elements_per_generation,
                            entity_lifespan,
                            no_improvement_max)

    print(f"Tempo Total rota = {cost}\n")
    print(f"Rota encontrada:\n")
    print_entity(route)

    print("Custo total:", cost + time)

    print(get_route(route))


if __name__ == "__main__":
    main()