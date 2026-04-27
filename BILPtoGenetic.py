#!/usr/bin/python3

import os, numpy as np

folderPath = input("Folder with BILP.dat files: ")

nts = 0
nu = 0
numFiles = 0
ratePerUser = []

for root, dirs, files in os.walk(folderPath, topdown=True):
    files.sort()
    for name in files:
        numFiles += 1
        fileName = os.path.join(root, name)
        print(fileName)
        with open(fileName, "r") as BILPFile:
            # Converte o nu
            for s in BILPFile.readline().strip("\n;").split():
                if s.isdigit():
                    nu = int(s)

            # Converte o nts
            for s in BILPFile.readline().strip("\n;").split():
                if s.isdigit():
                    nts = int(s)

            tsPerUser = []

            # Converte o num de timeslots pra cada user
            for s in BILPFile.readline().strip("\n;]").replace(',', "").replace('[', '').split():
                if s.isdigit() and s != '1':
                    tsPerUser.append(s)

            # Converte o num de timeslots pra cada user
            for s in BILPFile.readline().strip("\n;]").replace(',', "").replace('[', '').split():
                if s.replace('.', '').isdigit():
                    ratePerUser.append(s)

with open("convert_out.txt", "w") as outFile:
    outFile.write(f"{nts}\n")
    outFile.write(f"{nu}\n")
    for usr in tsPerUser:
        outFile.write(f"{usr} ")
    outFile.write("\n")

    arr = np.array(ratePerUser).reshape(numFiles, nu, nts)

    for k in range(numFiles):
        for i in range(nu):
            for j in range(nts):
                outFile.write(f"{arr[k][i][j]} ")
            outFile.write("\n")
        outFile.write("")