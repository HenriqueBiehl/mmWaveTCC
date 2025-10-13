#!/usr/bin/python3

import subprocess, os.path

OPLRUN_PATH="/opt/ibm/ILOG/CPLEX_Studio_Community2212/opl/bin/x86-64_linux/oplrun"
MODEL_PATH="./BILP.mod"
DATA_PATH="./BILP.dat"

if not os.path.isfile(OPLRUN_PATH):
    raise ValueError("OPL installation not found")
if not os.path.isfile(MODEL_PATH):
    raise ValueError("Model file not found")
if not os.path.isfile(DATA_PATH):
    raise ValueError("Data file not found")

subprocess.Popen(OPLRUN_PATH + ' ' + MODEL_PATH + ' ' + DATA_PATH + ' > output.txt', shell=True)
