import numpy as np
import genetic_scheduling as gs
import createPlot as cPlot
import sys, argparse, time

population_size = 700
num_generations = 100
elitism_rate = 0.01
tournament_size = 3
mutation_rate = 0.05

generations_metada = []

# Parseia entrada do programa
parser = argparse.ArgumentParser(description="Algoritmo Genético de Escalonamento em Redes mmWave")
parser.add_argument('-p', '--plot', action='store_true', help='Exibe o gráfico')
parser.add_argument('-fi', '--finalind', action='store_true', help='Exibe o(s) indivíduo(s) de fitness máximo ao final')
parser.add_argument('-c', '--convergence', action='store_true', help='Para o programa ao detectar convergencia')
parser.add_argument('-g', '--generations', type=int, help='Número de gerações para análise de convergência')
parser.add_argument('-t', '--threshold', type=float, help='Threshold de convergência')
args = parser.parse_args()

# Checa se criterios de convergencia estão corretos
if args.convergence:
    if args.generations is None or args.threshold is None:
        parser.error("Ao usar -c/--convergence, você deve informar -g e -t")

# Lê toda a entrada do arquivo ou stdin  
dados = sys.stdin.read().split()
dados = list(map(float, dados))  # converte tudo para float para facilitar

idx = 0
gene_size = int(dados[idx]); idx += 1   #Quantidade de scheduling sessions em um individuo
nts = int(dados[idx]); idx += 1         #Quantidade de timeslots por sessao
nu = int(dados[idx]); idx += 1          #Quantidade de usuários

print(f'Total timeslots:{nts}')
print(f'Total Users:{nu}')

user_nts_constraint = np.empty(nu) 
for i in range(0, nu):
    user_nts_constraint[i] = dados[idx] 
    idx += 1


print("User Timeslot usage:")
print(user_nts_constraint)
print("")

scheduling_sesssions_list = [] 
for k in range(0, gene_size):
    predicted_rate = np.empty((nu, nts))
    for i in range(0, nu):
        for j in range(0, nts):
            predicted_rate[i][j] = dados[idx] 
            idx += 1
    
    # print(f'Predicted rate for session {k}:')
    # print(predicted_rate)
    # print("") 

    scheduling_sesssions_list.append(predicted_rate)

scheduling_sesssions = np.array(scheduling_sesssions_list)

print("Scheduling session aggregation:")
print(scheduling_sesssions)
print("")


population = gs.initial_population_random(scheduling_sesssions.copy(), user_nts_constraint.copy(), gene_size, population_size, nts, nu)
population_copy = population.copy()

# print("Initial Population:")
# gs.print_population(population, population_size, gene_size,  nts)
# print("")

print("Crossover using Tournament and Session Swap Mutation")
max_fit = 0.0
avarege_fit = 0.0
lowest_fit = None
max_user = []
hypermutation = False
start = time.time()

gs.collect_generation_metadata(generations_metada, population, population_size)

for i in range(num_generations):
    new_population = gs.crossover(population, elitism_rate, tournament_size,  gene_size, population_size, nts, "roulette", "one-point")
    new_population = gs.timeslot_mutation(new_population, scheduling_sesssions, mutation_rate, gene_size, population_size, nts)

    gs.collect_generation_metadata(generations_metada, new_population, population_size)

    if (args.convergence) and (gs.check_convergence(generations_metada, i, args.generations, args.threshold)):
            print(f"GEN {i}: Convergence detected")
            gs.print_one_generation(generations_metada[i])
            if not hypermutation:
                new_population = gs.hypermutation(new_population, scheduling_sesssions.copy(), user_nts_constraint.copy(), gene_size, population_size, nts, nu)
                hypermutation = True
            else:
                break

    population = new_population.copy()

end = time.time() - start

print(f"Max fitness of generation {i+1} = {generations_metada[i]["max"]:.2f} found in {end:.2f} secs")

with open("metadata.txt", "w") as metadataFile:
    for g in generations_metada:
        metadataFile.write(f"{g['low']:.2f} - {g['avg']:.2f} - {g['max']:.2f}\n")

# print("Final Population:")
# gs.print_population(new_population, population_size, gene_size,  nts)
# print("")

if args.finalind:
    maxIndvs = []

    print("Maximal individuals: ")

    for p in population:
        nao_pertence = not any(np.array_equal(p, x) for x in maxIndvs)

        if (gs.fitness(p) == generations_metada[i]["max"]) and nao_pertence:
            maxIndvs.append(p)
            print("\t", end="")
            for j in range(gene_size):
                print(f"{p[j][0][0]}", end="")
            print("")

if args.plot:
    cPlot.plotFitness()