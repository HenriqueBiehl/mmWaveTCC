import numpy as np
import sys
import genetic_scheduling as gs

population_size = 700
num_generations = 100
elitism_rate = 0.2
tournament_size = 3
mutation_rate = 0.05

generations_metada = []

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

# print("Initial Population:")
# gs.print_population(population, population_size, gene_size,  nts)
# print("")

print("Crossover using Torunament and Session Swap Mutation")
print("\n")
max_fit = 0.0
avarege_fit = 0.0
lowest_fit = None
max_user = []
    
gs.collect_generation_metadata(generations_metada, population, population_size)

for i in range(num_generations):
    new_population = gs.crossover(population, elitism_rate, tournament_size,  gene_size, population_size, nts, "tournament", "uniform")
    new_population = gs.session_mutation(new_population, scheduling_sesssions, mutation_rate, gene_size, population_size, nts)

    gs.collect_generation_metadata(generations_metada, new_population, population_size)

    if(gs.check_convergence(generations_metada, i, 5, 25.0)):
            print(f"GEN {i}: Convergence detected")
            gs.print_one_generation(generations_metada[i])
            print("")

    population = new_population.copy()

# print("Final Population:")
# gs.print_population(new_population, population_size, gene_size,  nts)
# print("")
max_fit = 0.0
for j in range(population_size):
    f = gs.fitness(population[j])
    if f > max_fit:
        max_fit = f
        max_user = population[j]
print(f"Max fitness of generation {i+1} = {max_fit:.2f}")

print("Collected Fitness From All Generations")
gs.print_generation_metadata(generations_metada, num_generations)
# print("\t", end="")
# for i in range(gene_size):
#     print(f"{max_user[i][0][0]}", end="")
# print("")
