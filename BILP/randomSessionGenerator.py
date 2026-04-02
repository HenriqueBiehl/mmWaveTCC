#!/usr/bin/python3
import random

numTimeslots = int(input("Number of timeslots: "))
numUsers = int(input("Number of users: "))
maxAttenuation = int(input("Max. attenuation: "))
maxDistance = int(input("Max. distance: "))

with open("session.txt", "w") as sessionFile:
    sessionFile.write(f"{numTimeslots}\n")
    sessionFile.write(f"{numUsers}\n")
    sessionFile.write("2000000000\n")
    sessionFile.write("-71.99\n")
    sessionFile.write("62.5\n")
    sessionFile.write("0.2\n")
    sessionFile.write("6.7\n")
    sessionFile.write("20\n")
    sessionFile.write("3.16\n")
    sessionFile.write("0\n")
    sessionFile.write("63.4\n")
    sessionFile.write("1.72\n")
    sessionFile.write(f"{maxAttenuation}\n")
    for i in range(numUsers):
        for j in range(numTimeslots):
            sessionFile.write(f"{random.randrange(1, maxAttenuation)} ")
        sessionFile.write("\n")

    for i in range(numUsers):
        for j in range(numTimeslots):
            sessionFile.write(f"{random.randrange(1, maxDistance)} ")
        sessionFile.write("\n")