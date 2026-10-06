__all__ = [
    "map_load",
    "map_rows",
    "map_collumn",
    "map_tile_value",
    "map_gym_list",
    "map_start_pos",
    "map_end_pos",
    "map_find_gym",
    "map_get_neighbors_pos",
    "map_print",
]

TILE_COSTS = {"M": 200,
              "A": 30,
              "F": 15,
              "R": 5,
              ".": 1}
START_CHR = '1'
END_CHR = 'U'

_map_array = []
_map_rows = 0
_map_collumns = 0
_gym_array = []
    
def map_load(file_path : str) -> None:
    global _map_array, _map_rows, _map_collumns, _gym_array
    
    try:
        file = open(file_path, "r")
    except OSError as e:
        print("File with path %s could not be loaded", file_path)
        raise e

    lines = file.readlines()

    _map_rows = len(lines)
    _map_collumns = len(lines[0]) - 1

    for line in lines:
        for character in line:
            cost = TILE_COSTS.get(character)
            if character == '\n':
                continue
            if cost is None:
                cost = character
                if character not in [START_CHR, END_CHR]:
                    _gym_array.append(character)
            _map_array.append(cost)

    _gym_array.sort()

    file.close()

def map_rows() -> int:
    _check_for_map_init()
    return _map_rows

def map_collumn() -> int:
    _check_for_map_init()
    return _map_collumns

def map_tile_value(pos : tuple) -> int:
    _check_for_map_init()

    row = pos[0]
    collumn = pos[1]
    row, collumn = _map_negative_index(row, collumn)

    if row < 0 or row >= _map_rows:
        raise IndexError(f"Invalid index {row} {collumn}")
    elif collumn < 0 or collumn >= _map_collumns:
        raise IndexError(f"Invalid index {row} {collumn}")

    return _map_array[_map_collumns * row + collumn]

def map_gym_list():
    _check_for_map_init()
    return _gym_array.copy()

def map_start_pos() -> tuple:
    _check_for_map_init()

    return _map_find_char(START_CHR)

def map_end_pos() -> tuple:
    _check_for_map_init()
    
    return _map_find_char(END_CHR)

def map_find_gym(gym : str):
    _check_for_map_init()

    return _map_find_char(gym)

def map_get_neighbors_pos(pos : tuple) -> list:
    _check_for_map_init()
    
    neighbors = []

    row = pos[0]
    collumn = pos[1]
    row, collumn = _map_negative_index(row, collumn)

    if row != 0:
        neighbors.append((row - 1, collumn))
    if row != _map_rows - 1:
        neighbors.append((row + 1, collumn))
    if collumn != 0:
        neighbors.append((row, collumn - 1))
    if collumn != _map_collumns - 1:
        neighbors.append((row, collumn + 1))

    return neighbors
    
def map_print() -> None:
    _check_for_map_init()

    print(_map_rows)
    print(_map_collumns)
    print(_gym_array)

    for index, value in enumerate(_map_array):
        pos = _map_index_to_pos(index)
        if pos[1] == 0:
            print(f"{pos[0]} - ", end = "")

        print(f"{value} ", end="")

        if pos[1] == _map_collumns - 1:
            print()
            print()

def _check_for_map_init():
    if _map_array == []:
        raise Exception("No loaded map")

def _map_find_char(char : str):
    _check_for_map_init()

    chr_index = _map_array.index(char)
    return _map_index_to_pos(chr_index)

def _map_index_to_pos(index : int) -> tuple:
    row = index // _map_collumns
    collumn = index % _map_collumns
    return row, collumn

def _map_negative_index(row : int, collumn : int):

    if row < 0:
            row = _map_rows + row
    if collumn < 0:
        collumn = _map_collumns + collumn

    return row, collumn