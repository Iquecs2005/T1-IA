import pygame
import sys
from map import get_map, map_collumn, map_rows
from gym import get_gym_list


def setup_pygame() -> tuple[list, pygame.Surface]:
    global TILES, TILE_SIZE, PLAYER

    pygame.init()

    TILE_SIZE = 8

    map = get_map()
    collumns = map_collumn()
    rows = map_rows()
    map = [map[i: i + collumns] for i in range(0, len(map), collumns)]

    width = collumns * TILE_SIZE
    height = rows * TILE_SIZE

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pokemon Kanto map")

    PLAYER = pygame.image.load("tiles/red.png").convert()

    TILES = {
        200: pygame.image.load("tiles/mountain.png").convert(),
        30: pygame.image.load("tiles/water.png").convert(),
        15: pygame.image.load("tiles/forest.jpg").convert(),
        5: pygame.image.load("tiles/rock.png").convert(),
        1: pygame.image.load("tiles/grass.jpg").convert(),
        "1": pygame.image.load("tiles/home.png").convert(),
        "U": pygame.image.load("tiles/league.png").convert(),
        "gym": pygame.image.load("tiles/gym.png").convert()
    }

    for item in TILES:
        TILES[item] = pygame.transform.scale(TILES[item], (TILE_SIZE, TILE_SIZE))

    PLAYER = pygame.transform.scale(PLAYER, (TILE_SIZE, TILE_SIZE))

    return map, screen


def draw_map(screen: pygame.Surface, map: list):
    for y, line in enumerate(map):
        for x, tile in enumerate(line):
            image = TILES.get(tile)

            if tile in get_gym_list():
                image = TILES.get("gym")

            if image:
                screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))


def show_route(screen: pygame.Surface, map: list, route: list):
    route_index = 0
    wait = 1000
    last_move = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        time = pygame.time.get_ticks()

        if (time - last_move) >= wait and route_index < len(route) - 1:
            route_index += 1
            last_move = time

        draw_map(screen, map)

        y, x = route[route_index]
        screen.blit(PLAYER, (x * TILE_SIZE, y * TILE_SIZE))

        pygame.display.flip()
