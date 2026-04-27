#!/usr/bin/python3
import random

numTimeslots = int(input("Number of timeslots: "))
numUsers = int(input("Number of users: "))

minRate = 0.1
maxRate = 20.0

tsPerUser = int(numTimeslots/numUsers)

with open("BILP.dat", "w") as sessionFile:
    sessionFile.write(f"nu = {numUsers};\n")
    sessionFile.write(f"nts = {numTimeslots};\n")

    sessionFile.write("B = [")
    for i in range(numUsers):
        sessionFile.write(f"{tsPerUser}, ")
    for i in range(numTimeslots-1):
        sessionFile.write("1, ")
    sessionFile.write("1")
    sessionFile.write("];\n")

    sessionFile.write("R = [")
    for i in range((numUsers * numTimeslots) - 1):
        sessionFile.write(f"{round(random.uniform(minRate, maxRate), 2)}, ")
    sessionFile.write(f"{round(random.uniform(minRate, maxRate), 2)}")
    sessionFile.write("];\n")