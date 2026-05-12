#!/usr/bin/python3

import subprocess, os.path, re, argparse, time

def runner(DATA_PATH, show_x):
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

            if show_x: print(f"Objective = {objective:.2f} - x = {x}")
            else: print(f"Objective = {objective:.2f}")
        else:
            print("ERRO!!!!! Cheque output.txt")
            exit(0)

    return objective

def main():
    # Parseia entrada do programa
    parser = argparse.ArgumentParser(description="Algoritmo BILP de Escalonamento em Redes mmWave")
    parser.add_argument('-d', '--dir', help='Executa todos os arquivos de um diretorio')
    parser.add_argument('-f', '--file', help='Executa todos os arquivos de um diretorio')
    parser.add_argument('-x', '--x_result', action="store_true", help='Mostra o escalonamento final')
    args = parser.parse_args()

    start = time.perf_counter()

    obj = 0
    if args.dir:
        folderPath = args.dir
        for root, _, files in os.walk(folderPath, topdown=True):
            files.sort()
            for name in files:
                fileName = os.path.join(root, name)
                obj += runner(fileName, args.x_result)
    elif args.file:
        obj = runner(args.file, args.x_result)
    else:
        obj = runner('BILP.dat', args.x_result)

    end = time.perf_counter() - start

    print(f"Total Objective = {obj} Gbps")
    print(f"Results found in {end:.4f} secs")

if __name__ == '__main__':
    main()