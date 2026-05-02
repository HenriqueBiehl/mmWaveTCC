#!/usr/bin/python3

import subprocess, os.path, re, argparse, time

def runner(DATA_PATH):
    OPLRUN_PATH="/opt/ibm/ILOG/CPLEX_Studio2212/opl/bin/x86-64_linux/oplrun"
    MODEL_PATH="./BILP.mod"

    if not os.path.isfile(OPLRUN_PATH):
        raise ValueError("OPL installation not found")
    if not os.path.isfile(MODEL_PATH):
        raise ValueError("Model file not found")
    if not os.path.isfile(DATA_PATH):
        raise ValueError("Data file not found")

    proc = subprocess.Popen(OPLRUN_PATH + ' ' + MODEL_PATH + ' ' + DATA_PATH + ' > output.txt', shell=True)
    proc.wait()

    with open("output.txt", "r") as outputTXT:
        texto = outputTXT.read()

        match = re.search(r'Objective\s*=\s*([^\n]+).*?x\s*=\s*(\[[^\]]+\])', texto, re.S)

        if match:
            objective = float(match.group(1))
            x = match.group(2)

            print(f"Objective = {objective:.2f} - x = {x}")
        else:
            print("ERRO!!!!! Cheque output.txt")

def main():
    # Parseia entrada do programa
    parser = argparse.ArgumentParser(description="Algoritmo BILP de Escalonamento em Redes mmWave")
    parser.add_argument('-d', '--dir', help='Executa todos os arquivos de um diretorio')
    args = parser.parse_args()

    start = time.time()

    if args.dir:
        folderPath = args.dir
        for root, _, files in os.walk(folderPath, topdown=True):
            files.sort()
            for name in files:
                fileName = os.path.join(root, name)
                runner(fileName)
    else:
        runner('BILP.dat')

    end = time.time() - start

    print(f"Results found in {end} secs")

if __name__ == '__main__':
    main()