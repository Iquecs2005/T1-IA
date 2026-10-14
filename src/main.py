from map import *
from team import *
from team_ai import *

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


if __name__ == "__main__":
    main()
