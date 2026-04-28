import random 
import numpy as np
import sys


def gerar_user_nts_constraints(nu, nts):

    # começa com 1 em cada posição
    user_nts_constraint = [1] * nu

    restante = nts - nu

    # distribui o restante aleatoriamente
    for _ in range(restante):
        i = random.randint(0, nu - 1)
        user_nts_constraint[i] += 1

    return user_nts_constraint


min_rate = 0.1 
max_rate = 2.0

# Lê toda a entrada do arquivo ou stdin  
dados = sys.stdin.read().split()
dados = list(map(float, dados))  # converte tudo para float para facilitar

idx = 0
gene_size = int(dados[idx]); idx += 1
nts = int(dados[idx]); idx += 1
nu = int(dados[idx]); idx += 1

if(nu > nts):
    print("Numero de usuarios nao pode ser maior que total timeslots")
    sys.exit(1)

user_nts_constraint = gerar_user_nts_constraints(nu, nts)

scheduling_sesssions_list = [] 
user_nts_constraint_copy = user_nts_constraint.copy()
for k in range(0, gene_size):
    predicted_rate = np.empty((nu, nts))
    for i in range(0, nu):
        for j in range(0, nts):

            predicted_rate[i][j] =  random.uniform(min_rate, max_rate)
            idx += 1

    scheduling_sesssions_list.append(predicted_rate)

print(gene_size)
print(nts)
print(nu)
print(" ".join(map(str, user_nts_constraint )))
for i in range(0, gene_size):
    for j in range(0, nu):
        print(*(f"{x:.2f}" for x in scheduling_sesssions_list[i][j]))