import numpy as np
import sys, argparse, time
import random  

def validate_scheduling(scheduling, usage_constraint, nts, nu):

    user_usage_scheduling = [0]*nu

    for i in range(nts): 
        user_usage_scheduling[int(scheduling[i])] += 1
    
    for i in range(nu):
        if(user_usage_scheduling[i] != usage_constraint[i]):
            return 0

    return 1; 

def fitness(individual):
    return individual[:, 1, :].sum()

# Lê toda a entrada do arquivo ou stdin  
dados = sys.stdin.read().split()
dados = list(map(float, dados))  # converte tudo para float para facilitar

idx = 0
gene_size = int(dados[idx]); idx += 1   #Quantidade de scheduling sessions em um individuo
nts = int(dados[idx]); idx += 1         #Quantidade de timeslots por sessao
nu = int(dados[idx]); idx += 1          #Quantidade de usuários

print(f'Total Sessions: {gene_size}')
print(f'Total timeslots:{nts}')
print(f'Total Users:{nu}')

user_nts_constraint = np.empty(nu) 
for i in range(0, nu):
    user_nts_constraint[i] = int(dados[idx]) 
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

start_time = time.perf_counter()

schedule = []
for i in range(0, gene_size):
    scheduled_session = np.empty((2, nts))
    user_constraint_copy = user_nts_constraint.copy()
    for j in range(0, nts):
        
        max_user = None
        max_rate = 0 
        for k in range(0, nu): 
            if(scheduling_sesssions_list[i][k][j] > max_rate): 
                if(user_constraint_copy[k] > 0):
                    max_rate = scheduling_sesssions_list[i][k][j] 
                    max_user = k

        scheduled_session[0][j] = max_user 
        scheduled_session[1][j] = max_rate
        user_constraint_copy[max_user] -= 1 
    
    schedule.append(scheduled_session)

final_schedule = np.array(schedule)
    

end_time = time.perf_counter() - start_time

for i in range(0, gene_size):
    print(final_schedule[i][0])
    if(not validate_scheduling(final_schedule[i][0], user_nts_constraint, nts, nu)):
        print(f"Erro: scheduling {i} é inválido: ")
        print(final_schedule[i])
        exit(1)
print("Scheduling final válido!")

print(f"Max rate of greedy = {fitness(final_schedule/(10**9))} found in {end_time:.2f} secs")