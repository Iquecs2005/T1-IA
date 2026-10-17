from map import *
from team import *
from team_ai import *
from route_ai import *
from show_route import setup_pygame, show_route
from pathfinding import generate_distances_matrix, get_route

def main():
    simulations = 10

    initial_population_size = 750
    max_generations = 10000
    children_per_generation = 250
    new_elements_per_generation = 25
    entity_lifespan = 3
    no_improvement_max = 500

    team_list = []

    for i in range(simulations):
        team, time = simulate(initial_population_size,
                              max_generations,
                              children_per_generation,
                              new_elements_per_generation,
                              entity_lifespan,
                              no_improvement_max)

        print()
        print(f"Simulação {i + 1}\n")
        print(f"Tempo Total batalhas = {time}\n")
        print("Time encontrado:\n")
        print_team(team)

        team_list.append([team, time])

    team_mean = calculate_mean(team_list)
    team_std = calculate_std(team_list, team_mean)
    team_min, team_min_value = get_min_value(team_list)

    print("Resumo:\n")
    print(f"Numero de simulações: {simulations}")
    print(f"Media: {team_mean}")
    print(f"Desvio padrão: {team_std}")
    print(f"Melhor tempo: {team_min_value}")
    print("Melhor time:\n")
    print_team(team_min)

    map_load("maps/Kanto.txt")

    set_gym_amount(24)
    set_distances(generate_distances_matrix(get_map(), map_start_pos(), map_end_pos()))

    routes_list = []

    for i in range(simulations):
        route, cost = simulate_route(initial_population_size,
                                max_generations,
                                children_per_generation,
                                new_elements_per_generation,
                                entity_lifespan,
                                no_improvement_max)
        routes_list.append([route, cost])

    route_mean = calculate_mean(routes_list)
    route_std = calculate_std(routes_list, route_mean)
    route_min, route_min_value = get_min_value(routes_list)

    print("Resumo:\n")
    print(f"Numero de simulações: {simulations}")
    print(f"Media: {route_mean}")
    print(f"Desvio padrão: {route_std}")
    print(f"Melhor tempo: {route_min_value}")
    print("Melhor rota:\n")
    print_entity(route_min)

    print("Custo total:", cost + time)

    path = get_route(route)

    map, screen = setup_pygame()
    show_route(screen, map, path)


def calculate_mean(list):
    mean = 0
    for value in list:
        mean += value[1]

    mean /= len(list)
    return mean


def calculate_std(list, mean):
    std = 0
    for value in list:
        std += (value[1] - mean) ** 2
    std = (std / len(list)) ** (1/2)
    return std


def get_min_value(list):
    min_value = list[0][1]
    min_team = list[0][0]
    for value in list[1:]:
        if value[1] < min_value:
            min_team = value[0]
            min_value = value[1]
    return min_team, min_value


if __name__ == "__main__":
    main()
