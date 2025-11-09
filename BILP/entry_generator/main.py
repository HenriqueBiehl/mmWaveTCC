import numpy as np

nts = int(input())          #Total Timeslots
n = int(input())            #Total Users
b = float(input())          #Bandwidth 
pn = float(input())         #Noise power
delta_ts = float(input())   #Scheduling time slot lenght
ro_D = float(input())       #Decay factor
ro_R = float(input())       #Rise factor
ptx = float(input())        #Transmitter power
gtx = float(input())        #Transmitter gain
grx = float(input())        #Receiver gain
l0  = float(input())        #Path loss reference
v   = float(input())        #Attenuation exponent
Amax = float(input())       #Maximum attenuation

# --- conversões ---
ptx = 10**(ptx/10) / 1000
gtx = 10**(gtx/10)
grx = 10**(grx/10)
l0 = 10**(-l0/10)
Amax = 10**(Amax/10)
pn = 10**(pn/10) / 1000

attenuation_str = []
attenuation_factor = np.zeros((n, nts))
for i in range(0, n):
    attenuation_str.append(input())
    attenuation_factor[i] = np.fromstring(attenuation_str[i], sep=' ', dtype=np.float64)

print("Attenuation factor:")
print(attenuation_factor)
print("")

distance_str = []
distance_AP = np.zeros((n, nts))
for i in range(0, n):
    distance_str.append(input())
    distance_AP[i] = np.fromstring(distance_str[i], sep=' ', dtype=np.float64)

print("Distances from AP:")
print(distance_AP)
print("")

print("Simulation parameters:")
print(f'Bandiwidth: {b:.2f}')
print(f'Noise Power: {pn:.20f}')
print(f'Decay Factor: {ro_D:.2f}')
print(f'Rise Factor: {ro_R:.2f}')
print(f'Transmitter Power: {ptx:.2f}')
print(f'Transmitter Gain: {gtx:.2f}')
print(f'Receiver Gain: {grx:.2f}')
print(f'Path Loss Reference: {l0:.2f}')
print(f'Attenuation Exponent: {v:.2f}')
print(f'Maximum Attenuation: {Amax:.2f}')
print("")

# Matrix A
A = np.zeros((n+nts, n*nts), dtype=np.int64)

# First Nu rows (indices começam em 1 -> 1-based)
for k in range(1, n+1):
    for q in range(1, (n*nts)+1):
        if ((q > (k-1)*nts) and (q <= k*nts)):
            A[k-1][q-1] = 1
        else:
            A[k-1][q-1] = 0

# Last Nts Rows (indices começam em 1 -> 1-based)
for k in range (n+1, n+nts+1):
    for q in range (1, (n*nts)+1):
        if (q == k-n) or (q == k-n+nts): A[k-1][q-1] = 1

print("A = " + np.array2string(A, separator=', '))
print("")

# Vector B
B = np.zeros((n+nts), dtype=np.int64)

# First Nu rows (indices começam em 1 -> 1-based) = Number of time slots to each user
# !!! ATENCAO !!! AQUI DEVERIA VIR DE ALGUM LUGAR A QTD DE TIMESLOTS PRA CADA USER
for k in range(1, n+1): B[k-1] = nts/n

# Last Nts Rows (indices começam em 1 -> 1-based) = 1
for k in range (n+1, n+nts+1): B[k-1] = 1

print("B = " + np.array2string(B, separator=', '))
print("")

# Vector R
R = np.zeros((n,nts), dtype=np.float64)

# Calculate each R
for i in range(0, n):
    for j in range(0, nts):
        prx = (ptx * gtx * grx * l0 * np.power(distance_AP[i][j], -v)) / attenuation_factor[i][j]
        r = b * np.log2(1 + prx/pn)
        R[i][j] = r / 1e9

R = R.flatten()
print("R = " + np.array2string(R, separator=', ', formatter={'float_kind':lambda x: f"{x:.2f}"}))
print("")

# Write to output file
with open("BILP.dat", "w") as file:
    file.write("m = " + str(nts+n) + ";\n")
    file.write("n = " + str(nts*n) + ";\n")
    file.write("A = " + np.array2string(A, separator=', ') + ";\n")
    file.write("B = " + np.array2string(B, separator=', ') + ";\n")
    file.write("R = " + np.array2string(R, separator=', ', formatter={'float_kind':lambda x: f"{x:.2f}"}) + ";\n")