import heapq
from map import *
from gym import *
from map_node import map_node


def manhattan_distance(origin: tuple[int, int], dst: tuple[int, int]) -> int:
    distance = abs(origin[0] - dst[0]) + abs(origin[1] - dst[1])
    return distance


def reconstruct_path(dst: map_node) -> list[tuple[int, int]]:
    path = []
    curr_node = dst

    while curr_node:
        path.append(curr_node.get_coord())
        curr_node = curr_node.get_parent()

    return path[::-1]


def get_route(path: list) -> list[tuple[int, int]]:
    total_path = []
    curr_pos = map_start_pos()

    map = get_map()

    for i in path:
        total_path += pathfinder(map, curr_pos, map_find_gym(i))[0]
        curr_pos = map_find_gym(i)

    total_path += pathfinder(map, curr_pos, map_end_pos())[0]
    return total_path


def pathfinder(map: list, origin: tuple[int, int], dst: tuple[int, int]) -> tuple[list, int]:
    start = map_node(origin, 0, manhattan_distance(origin, dst))
    open_nodes = [(start.get_fx(), start)]
    open_dict = {start.get_coord(): start}
    closed_nodes = []
    gym_list = get_gym_list()

    while open_nodes:
        current_node = heapq.heappop(open_nodes)[1]

        if current_node.get_coord() in closed_nodes:
            continue

        if current_node.get_coord() == dst:
            return reconstruct_path(current_node), current_node.get_gx()

        closed_nodes.append(current_node.get_coord())

        for neighbor in map_get_neighbors_pos(current_node.get_coord()):
            if neighbor in closed_nodes:
                continue

            tile_value = map_tile_value(neighbor)
            if tile_value in gym_list or tile_value == 'U':
                tile_value = 0
            neighbor_g = int(tile_value) + current_node.get_gx()
            neighbor_h = manhattan_distance(neighbor, dst)
            neighbor_parent = current_node

            if neighbor not in open_dict:
                neighbor_node = map_node(neighbor, neighbor_g, neighbor_h)
                neighbor_node.set_parent(neighbor_parent)
                heapq.heappush(open_nodes, (neighbor_node.get_fx(), neighbor_node))
                open_dict[neighbor] = neighbor_node
            elif neighbor_g < open_dict[neighbor].get_gx():
                neighbor_node = open_dict[neighbor]
                neighbor_node.set_gx(neighbor_g)
                neighbor_node.set_fx(neighbor_g + neighbor_node.get_hx())
                neighbor_node.set_parent(neighbor_parent)
                heapq.heappush(open_nodes, (neighbor_node.get_fx(), neighbor_node))

    return [], 0


def generate_distances_matrix(map: list, origin: tuple[int, int], dst: tuple[int, int]) -> list:
    points = []

    points.append(origin)
    for i in get_gym_list():
        points.append(map_find_gym(i))
    points.append(dst)

    distances = [[0 for i in range(len(points))] for j in range(len(points))]
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            path, cost = pathfinder(map, points[i], points[j])
            distances[i][j] = cost
            distances[j][i] = cost

    return distances
