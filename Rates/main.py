
import sys
import numpy as np
import random 
import math

def gerar_user_nts_constraints(nu, nts):

    # começa com 1 em cada posição
    user_nts_constraint = [1] * nu

    restante = nts - nu

    # distribui o restante aleatoriamente
    for _ in range(restante):
        i = random.randint(0, nu - 1)
        user_nts_constraint[i] += 1

    return user_nts_constraint


sigma = 0.1
# Lê toda a entrada do arquivo ou stdin  
dados = sys.stdin.read().split()
dados = list(map(float, dados))  # converte tudo para float para facilitar

idx = 0
gene_size = int(dados[idx]); idx += 1   #Quantidade de scheduling sessions em um individuo
nts = int(dados[idx]); idx += 1         #Quantidade de timeslots por sessao
nu = int(dados[idx]); idx += 1          #Quantidade de usuários
bl = float(dados[idx]); idx += 1 
pn = float(dados[idx]); idx += 1 
ptx= float(dados[idx]); idx += 1 
gtx = float(dados[idx]); idx += 1 
grx = float(dados[idx]); idx += 1 
l0 = float(dados[idx]); idx += 1 
v = float(dados[idx]); idx += 1 
Amax = float(dados[idx]); idx += 1 
lambaB = float(dados[idx]); idx += 1 
tauB = float(dados[idx]); idx += 1 

user_distances = np.empty(nu) 
for i in range(0, nu ):
    user_distances[i] = random.uniform(0.1, 10)
    idx += 1

user_nts_constraint = gerar_user_nts_constraints(nu, nts)


predicted_rates = []
for i in range(0, gene_size):

    session = []
    for j in range(0, nu): 
        
        blocked_until = 0 
        if(random.uniform(0, 1) < lambaB):
            blocked_until = tauB

        next_block = np.random.exponential(1/lambaB)
        blocked_until = np.random.exponential(tauB)

        user_rates = []
        error = np.random.normal(loc=0.0, scale=sigma, size=nts)
        for k in range(0, nts): 

            fading = np.random.lognormal(0, 0.2)

            prx = (
                ptx *
                gtx *
                grx *
                l0 *
                fading *
                user_distances[j]**(-v)
            )

            if(blocked_until > 0):
                #print(f'down on {j}:{k}')
                prx = prx/Amax 
                blocked_until -= 1
            
            E = error[k]
            r = bl * math.log2(1 + ((prx + E )/pn))
            user_rates.append(r)

        session.append(user_rates)
        
    predicted_rates.append(session)


    for i in range(0, nu ):
        min = 0 if user_distances[i] == 0.1 else -user_distances[i] + 0.1
        user_distances[i] += random.uniform(min, 0.5)


print(gene_size)
print(nts)
print(nu)
print(" ".join(map(str, user_nts_constraint )))

for i in range(0, gene_size):
    for j in range(0, nu): 
        print(*(f"{x:.2f}" for x in predicted_rates[i][j]))

