
import sys
import numpy as np
import random 
import math

# Lê toda a entrada do arquivo ou stdin  
dados = sys.stdin.read().split()
dados = list(map(float, dados))  # converte tudo para float para facilitar

idx = 0
gene_size = int(dados[idx]); idx += 1   #Quantidade de scheduling sessions em um individuo
nts = int(dados[idx]); idx += 1         #Quantidade de timeslots por sessao
nu = int(dados[idx]); idx += 1          #Quantidade de usuários
b = float(dados[idx]); idx += 1 
pn = float(dados[idx]); idx += 1 
ptx= float(dados[idx]); idx += 1 
gtx = float(dados[idx]); idx += 1 
grx = float(dados[idx]); idx += 1 
l0 = float(dados[idx]); idx += 1 
v = float(dados[idx]); idx += 1 
Amax = float(dados[idx]); idx += 1 
lambaB = float(dados[idx]); idx += 1 
tauB = float(dados[idx]); idx += 1 


print(f'Total Sessions: {gene_size}')
print(f'Total timeslots:{nts}')
print(f'Total Users:{nu}')

user_distances = np.empty(nu) 
for i in range(0, nu ):
    user_distances[i] = random.uniform(0.1, 10)
    idx += 1

user_nts_constraint = [0] * nu
for i in range(0, nu):
    user_nts_constraint[i] = nts/nu 

predicted_rates = []
for i in range(0, gene_size):

    session = []
    for j in range(0, nu): 
        
        blocked_until = 0 
        if(random.uniform(0, 1) < lambaB):
            blocked_until = tauB

        user_rates = []
        for k in range(0, nts): 
            prx = (ptx * gtx * grx * l0 * (user_distances[j] ** -v ) )

            if(blocked_until != 0):
                
                prx = prx/Amax 
                blocked_until -= 1
            
            r = b * math.log2(1 + (prx/pn))

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

