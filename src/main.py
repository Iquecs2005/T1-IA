from map import *
from team import *
from team_ai import *
from route_ai import *
from show_route import setup_pygame, show_route
from pathfinding import generate_distances_matrix, get_route

def main():
    simulations = 10

    initial_population_size = 500
    max_generations = 500
    children_per_generation = 150
    new_elements_per_generation = 10
    entity_lifespan = 3
    no_improvement_max = 20

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

    mean = 0
    for value in team_list:
        mean += value[1]

    mean /= len(team_list)

    std = 0
    for value in team_list:
        std += (value[1] - mean) ** 2
    std = (std / len(team_list)) ** (1/2)

    min_value = team_list[0][1]
    min_team = team_list[0][0]
    for value in team_list[1:]:
        if value[1] < min_value:
            min_team = value[0]
            min_value = value[1]

    print("Resumo:\n")
    print(f"Numero de simulações: {simulations}")
    print(f"Media: {mean}")
    print(f"Desvio padrão: {std}")
    print(f"Melhor tempo: {min_value}")
    print("Melhor time:\n")
    print_team(min_team)

    map_load("maps/Kanto.txt")

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

    path = get_route(route)
    print(path)

    map, screen = setup_pygame()
    show_route(screen, map, path)


if __name__ == "__main__":
    main()
