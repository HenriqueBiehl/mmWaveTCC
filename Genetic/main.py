import numpy as np
import sys
import genetic_scheduling as gs

gene_size = 2
initial_population = 5

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

print("Crossover:")
new_population = gs.crossover(population, 0.5, gene_size, initial_population, nts)
gs.print_population(new_population, initial_population, gene_size, nts)
print("")

print("Mutation (Session):")
new_population = gs.session_mutation(new_population, scheduling_sesssions, 0.3, gene_size, initial_population, nts)
gs.print_population(new_population, initial_population, gene_size, nts)
print("")