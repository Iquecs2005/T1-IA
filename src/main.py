from map import *

def main():
    map_load("maps\kanto.txt")
    map_print()
    print(map_rows())
    print(map_collumn())
    print(map_tile_value((-1, -1)))
    print(map_start_pos())
    print(map_tile_value((23, 35)))
    print(map_end_pos())
    print(map_tile_value((1, 16)))
    print(map_gym_list())
    print(map_find_gym("8"))
    print(map_tile_value((14,117)))
    print(map_get_neighbors_pos((-1,-1)))


if __name__ == "__main__":
    main()