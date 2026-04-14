import numpy as np
import sys
import genetic_scheduling as gs

gene_size = 2
initial_population = 5
num_generations = 1000
elitism_rate = 0.2
mutation_rate = 0.2

# Lê toda a entrada do arquivo ou stdin  
dados = sys.stdin.read().split()
dados = list(map(float, dados))  # converte tudo para float para facilitar

idx = 0
nts = int(dados[idx]); idx += 1
nu = int(dados[idx]); idx += 1

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
    
    print(f'Predicted rate for session {k}:')
    print(predicted_rate)
    print("") 

    scheduling_sesssions_list.append(predicted_rate)

scheduling_sesssions = np.array(scheduling_sesssions_list)

print("Scheduling session aggregation:")
print(scheduling_sesssions)
print("") 


population = gs.initial_population_random(scheduling_sesssions.copy(), user_nts_constraint.copy(), gene_size, initial_population, nts, nu)

print("Initial Population:")
gs.print_population(population, initial_population, gene_size,  nts)
print("")

max_fit = 0.0
max_user = []
for i in range(num_generations):
    new_population = gs.crossover(population, elitism_rate, gene_size, initial_population, nts, "roulette")
    new_population = gs.session_mutation(new_population, scheduling_sesssions, mutation_rate, gene_size, initial_population, nts)

    for j in range(initial_population):
        f = gs.fitness(new_population[j], gene_size, nts)
        if f > max_fit:
            max_fit = f
            max_user = new_population[j]

    population = new_population.copy()

    # print(f"Max fitness of generation {i} = {max_fit:.2f}")
    # print(f"\t{max_user[0][0][0]}{max_user[1][0][0]}")

# print("Final Population:")
# gs.print_population(new_population, initial_population, gene_size,  nts)
# print("")

print(f"Max fitness of generation {i+1} = {max_fit:.2f}")
print(f"\t{max_user[0][0][0]}{max_user[1][0][0]}")