import numpy as np
import heuristic_scheduler as hs
import sys

# Lê toda a entrada do arquivo ou stdin
dados = sys.stdin.read().split()
dados = list(map(float, dados))  # converte tudo para float para facilitar

idx = 0
nts = int(dados[idx]); idx += 1
n = int(dados[idx]); idx += 1
threshold = float(dados[idx]); idx += 1

print(f'Total timeslots:{nts}')
print(f'Total Users:{n}')
print(f'Threshold:{threshold}')

rate_u = np.empty((n, nts)) 
for i in range(0, n):
    for j in range(0, nts):
        rate_u[i][j] = dados[idx] 
        idx += 1


status_u = np.empty((n, nts))
for i in range(0, n):
    for j in range(0, nts):
        status_u[i][j] = 1 if rate_u[i][j] <= threshold else 0

allot_u = np.empty(n)
for i in range(0, n):
    allot_u[i] =  int(dados[idx]) 
    idx += 1


print("User Rate table:")
print(rate_u)
print("")


print("User Low rate status table:")
print(status_u)
print("")

print("User Allotment table:")
print(allot_u)
print("")

X = hs.heuristic_scheduler(rate_u, status_u, allot_u, n, nts)

print("User Scheduled table:")
print(X)
print("")