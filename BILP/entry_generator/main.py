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

ts_assigment_table = np.empty((n, nts))
distance_AP = np.empty((n)); 

for i in range(0, n):
    distance_AP[i] = float(input())

ent = input()
for i in range(0, n):
    ts_assigment_table[i,:] = np.array(list(map(int, ent.split())))


print("Assigment table:")
print(ts_assigment_table)
print("")

print("Distance from AP:")
print(distance_AP)
print("")

print("Simulation parameters:")
print(f'Bandiwidth: {b:.2f}')
print(f'Noise Power: {pn:.2f}')
print(f'Decay Factor: {ro_D:.2f}')
print(f'Rise Factor: {ro_R:.2f}')
print(f'Transmitter Power: {ptx:.2f}')
print(f'Transmitter Gain: {gtx:.2f}')
print(f'Receiver Gain: {grx:.2f}')
print(f'Path Loss Reference: {l0:.2f}')
print(f'Attenuation Exponent: {v:.2f}')
print(f'Maximum Attenuation: {Amax:.2f}')

