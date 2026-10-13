from map import *
from team_ai import *

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

    for i in range(2):
        entity, time = simulate(initial_population_size = 5000,
                                max_generations = 1000,
                                children_per_generation = 1000,
                                new_elements_per_generation = 1000,
                                entity_lifespan = 5,
                                no_improvement_max = 15)

        print(f"Battle min time = {time}\n")
        print(f"Entity:\n")
        print_entity(entity)


if __name__ == "__main__":
    main()