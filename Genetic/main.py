import numpy as np
import sys
import genetic_scheduling as gs

population_size = 5
num_generations = 50
elitism_rate = 0.2
tournament_size = 3
mutation_rate = 0.2

# Lê toda a entrada do arquivo ou stdin  
dados = sys.stdin.read().split()
dados = list(map(float, dados))  # converte tudo para float para facilitar

idx = 0
gene_size = int(dados[idx]); idx += 1   #Quantidade de scheduling sessions em um individuo
nts = int(dados[idx]); idx += 1         #Quantidade de timeslots por sessao
nu = int(dados[idx]); idx += 1          #Quantidade de usuários

print(f'Total timeslots:{nts}')
print(f'Total Users:{nu}')

user_nts_constraint = np.empty(nu) 
for i in range(0, nu):
    user_nts_constraint[i] = dados[idx] 
    idx += 1


print("User Timeslot usage:")
print(user_nts_constraint)
print("")

scheduling_sesssions_list = [] 
for k in range(0, gene_size):
    predicted_rate = np.empty((nu, nts))
    for i in range(0, nu):
        for j in range(0, nts):
            predicted_rate[i][j] = dados[idx] 
            idx += 1
    
    # print(f'Predicted rate for session {k}:')
    # print(predicted_rate)
    # print("") 

    scheduling_sesssions_list.append(predicted_rate)

scheduling_sesssions = np.array(scheduling_sesssions_list)

print("Scheduling session aggregation:")
print(scheduling_sesssions)
print("") 


population = gs.initial_population_random(scheduling_sesssions.copy(), user_nts_constraint.copy(), gene_size, population_size, nts, nu)
population_copy = population.copy()

print("Initial Population:")
gs.print_population(population, population_size, gene_size,  nts)
print("")

print("Crossover using Roulette and Session Swap Mutation")
print("\n")
max_fit = 0.0
max_user = []
for i in range(num_generations):
    new_population = gs.crossover(population, elitism_rate, tournament_size,  gene_size, population_size, nts, "roulette")
    new_population = gs.session_mutation(new_population, scheduling_sesssions, mutation_rate, gene_size, population_size, nts)

    for j in range(population_size):
        f = gs.fitness(new_population[j], gene_size, nts)
        if f > max_fit:
            max_fit = f
            max_user = new_population[j]

    population = new_population.copy()

    # print(f"Max fitness of generation {i+1} = {max_fit:.2f}")
    # print(f"\t{max_user[0][0][0]}{max_user[1][0][0]}")

# print("Final Population:")
# gs.print_population(new_population, population_size, gene_size,  nts)
# print("")

print(f"Max fitness of generation {i+1} = {max_fit:.2f}")
print(f'Avarege User Data Rate ({gene_size} sessions): {(max_fit/nu):.2f}')
print(f'Avarege User Data Rate Per Session: {(max_fit/(nu*gene_size)):.2f}')
#print("\t", end="")
print("Fittest individual: \n")
gs.print_individual(max_user, gene_size, nts)

# for i in range(gene_size):
#     gs.print_individual(max_user, gene_size, nts)
# print("")
#gs.print_population(new_population, population_size, gene_size, nts)
print("")

population = population_copy.copy()

print("Crossover using Tournament and Timeslot Swap Mutation")
print("\n")

max_fit = 0.0
max_user = []
for i in range(num_generations):
    new_population = gs.crossover(population, elitism_rate, tournament_size,  gene_size, population_size, nts, "tournament")
    new_population = gs.timeslot_mutation(new_population, scheduling_sesssions, mutation_rate, gene_size, population_size, nts)

    for j in range(population_size):
        f = gs.fitness(new_population[j], gene_size, nts)
        if f > max_fit:
            max_fit = f
            max_user = new_population[j]

    population = new_population.copy()

    # print(f"Max fitness of generation {i+1} = {max_fit:.2f}")
    # print(f"\t{max_user[0][0][0]}{max_user[1][0][0]}")

# print("Final Population:")
# gs.print_population(new_population, population_size, gene_size,  nts)
# print("")

print(f"Max fitness of generation {i+1} = {max_fit:.2f}")
print(f'Avarege User Data Rate ({gene_size} sessions): {(max_fit/nu):.2f}')
print(f'Avarege User Data Rate Per Session: {(max_fit/(nu*gene_size)):.2f}')


#print("\t", end="")
print("Fittest individual: \n")
gs.print_individual(max_user, gene_size, nts)

# for i in range(gene_size):
#     gs.print_individual(max_user, gene_size, nts)
# print("")
#gs.print_population(new_population, population_size, gene_size, nts)
print("")



# print("Crossover Roulette:")
# new_population = gs.crossover(population, elitism_rate, tournament_size, gene_size, population_size, nts, "roulette")
# gs.print_population(new_population, population_size, gene_size, nts)
# print("")

# print("Crossover Tournament:")
# new_population = gs.crossover(population, elitism_rate, tournament_size, gene_size, population_size, nts, "tournament")
# gs.print_population(new_population, population_size, gene_size, nts)
# print("")


# print("Mutation by Timeslot Swap")
# index = gs.mutation_operator(new_population, population_size, gene_size, scheduling_sesssions, nts, gs.mutation_swap_timeslot)
# print(f'new ind{index}:')
# gs.print_individual(new_population[index], gene_size, nts)
# print("")



