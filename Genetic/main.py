import numpy as np
import genetic_scheduling as gs
import createPlot as cPlot
import sys, argparse, time
import random  


population_size = 5
num_generations = 30000
elitism_rate = 0.2
tournament_size = 2
crossover_rate = 1.0
mutation_rate = 0.15

generations_metada = []

# Parseia entrada do programa
parser = argparse.ArgumentParser(description="Algoritmo Genético de Escalonamento em Redes mmWave")
parser.add_argument('-p', '--plot', action='store_true', help='Exibe o gráfico')
parser.add_argument('-fi', '--finalind', action='store_true', help='Exibe o(s) indivíduo(s) de fitness máximo ao final')
parser.add_argument('-c', '--convergence', action='store_true', help='Para o programa ao detectar convergencia')
parser.add_argument('-g', '--generations', type=int, help='Número de gerações para análise de convergência')
parser.add_argument('-mc', '--max_conv', type=int, help='Número máximo de vezes que irá convergir antes de parar')
parser.add_argument('-t', '--threshold', type=float, help='Threshold de convergência')
parser.add_argument('-meta ', '--metadata', action='store_true', help='Retorna, ao fim da execução, os metadados e parametros utilizados')
parser.add_argument('-s', '--seed', action='store_true', help='Adicionar seed manualmente')
parser.add_argument('-sv', '--seed_value', type=int, help='Valor da seed')
parser.add_argument('-tl', '--time_limit', type=float, help='Limite de tempo')

#Adicionar opcao -m que printa os metadados utilizados (tamanho populacao, geracoes, eltitimos, seed utilizada no programa, etc)
#adiciona opcao -s que utiliza uma seed passada por argumento 
args = parser.parse_args()

# Checa se criterios de convergencia estão corretos
if args.convergence:
    if args.generations is None or args.threshold is None or args.max_conv is None:
        parser.error("Ao usar -c/--convergence, você deve informar -g, -t e -mc")

if args.seed:
    if args.seed is None:
            parser.error("Ao usar -s/--seed, você deve informar -sv e indicar o valor da seed")
    else:
        print(f'Used seed: {args.seed_value}')
        exec_seed = args.seed_value
else:
    exec_seed = random.randrange(sys.maxsize)

random.seed(exec_seed)


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


#population = gs.initial_population_random(scheduling_sesssions.copy(), user_nts_constraint.copy(), gene_size, population_size, nts, nu)
population = gs.initial_population_replicated_gene(scheduling_sesssions.copy(), user_nts_constraint.copy(), gene_size, population_size, nts, nu)
population_copy = population.copy()

# print("Initial Population:")
# gs.print_population(population, population_size, gene_size,  nts)
# print("")

print("Crossover using Roulette, Session Swap Mutation and One-Point Crossover")
last_convergence = 0
conv_count = 0
start = time.perf_counter()

if (args.plot) or (args.convergence): gs.collect_generation_metadata(generations_metada, population, population_size)

new_population = population_copy
if args.time_limit == None:
    for i in range(num_generations):
        r = random.uniform(0, 1)
        if(r < crossover_rate):
            new_population = gs.crossover(population, elitism_rate, tournament_size,  gene_size, population_size, nts, "roulette", "one-point", "renewall")
        
        new_population = gs.timeslot_mutation(new_population, scheduling_sesssions, mutation_rate, gene_size, population_size, nts)

        if (args.plot) or (args.convergence) or (i == num_generations-1): gs.collect_generation_metadata(generations_metada, new_population, population_size)
        
        if (args.convergence) and (gs.check_convergence(generations_metada, i, args.generations, args.threshold, last_convergence)):
            print(f"GEN {i}: Convergence detected")
            gs.print_one_generation(generations_metada[i])
            new_population = gs.hypermutation(new_population, scheduling_sesssions.copy(), user_nts_constraint.copy(), gene_size, population_size, nts, nu, 0.5)
            last_convergence = i
            conv_count += 1

        # Hipermutação no max max_conv vezes, depois para o algoritmo pela convergencia
        if conv_count == args.max_conv:
            break

        population = new_population.copy()
else:
    i = 0
    while(True):
        r = random.uniform(0, 1)
        if(r < crossover_rate):
            new_population = gs.crossover(population, elitism_rate, tournament_size,  gene_size, population_size, nts, "roulette", "one-point", "renewall")
        
        new_population = gs.timeslot_mutation(new_population, scheduling_sesssions, mutation_rate, gene_size, population_size, nts)

        if (args.plot) or (args.convergence): gs.collect_generation_metadata(generations_metada, new_population, population_size)
        
        if (args.convergence) and (gs.check_convergence(generations_metada, i, args.generations, args.threshold, last_convergence)):
            print(f"GEN {i}: Convergence detected")
            gs.print_one_generation(generations_metada[i])
            new_population = gs.hypermutation(new_population, scheduling_sesssions.copy(), user_nts_constraint.copy(), gene_size, population_size, nts, nu, 0.5)
            last_convergence = i
            conv_count += 1

        # Hipermutação no max max_conv vezes, depois para o algoritmo pela convergencia
        if conv_count == args.max_conv:
            break

        population = new_population.copy()
        i += 1

        elapsed_time  = time.perf_counter() - start
        if elapsed_time >= args.time_limit:
            gs.collect_generation_metadata(generations_metada, new_population, population_size)
            break

end = time.perf_counter() - start

if args.plot:
    print(f"Max fitness of generation {i+1} = {generations_metada[i]['max']:.2f} found in {end:.2f} secs")
    with open("metadata.txt", "w") as metadataFile:
        for g in generations_metada:
            metadataFile.write(f"{g['low']:.2f} - {g['avg']:.2f} - {g['max']:.2f}\n")
else:
    print(f"Max fitness of generation {i+1} = {generations_metada[0]['max']:.2f} found in {end:.2f} secs")

# print("Final Population:")
# gs.print_population(new_population, population_size, gene_size,  nts)
# print("")

if args.finalind:
    maxIndvs = []

    print("Maximal individuals: ")

    for p in population:
        nao_pertence = not any(np.array_equal(p, x) for x in maxIndvs)

        if args.plot:
            if (gs.fitness(p) == generations_metada[idx]["max"]) and nao_pertence:
                maxIndvs.append(p)
                print("\t", end="")
                for j in range(gene_size):
                    print(f"{p[j][0]}", end="")
                print("")
        else:
            if (gs.fitness(p) == generations_metada[0]["max"]) and nao_pertence:
                maxIndvs.append(p)
                print("\t", end="")
                for j in range(gene_size):
                    print(f"{p[j][0]}", end="")
                print("")

if args.plot:
    cPlot.plotFitness()

if args.metadata:
    print("\n")
    print("---- Metadata and Parameters -----")
    print(f"    Seed: {exec_seed}")
    print(f"    Population size: {population_size}")
    print(f"    Generation Number: {num_generations}")
    print(f"    Elitism Rate: {elitism_rate:.2f}")
    print(f"    Mutation Rate: {mutation_rate:.2f}")
    print(f"    Tournament Size: {tournament_size}")

    if(args.convergence):
        print(f"    Converge Maximum Count: {args.max_conv}")
        print(f"    Convergence Generation Threshold: {args.generations}")
        print(f"    Convergence Threshold: {args.threshold:.2f}")
 