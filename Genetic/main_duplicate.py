import numpy as np
import genetic_scheduling as gs
import createPlot as cPlot
import sys, argparse, time
import random  


population_size = 10
num_generations = 100000
elitism_rate = 0.2
tournament_size = 2
crossover_rate = 1.0
mutation_rate = 0.3


# Parseia entrada do programa
parser = argparse.ArgumentParser(description="Algoritmo Genético de Escalonamento em Redes mmWave")
parser.add_argument('-p', '--plot', action='store_true', help='Exibe o gráfico')
parser.add_argument('-fi', '--finalind', action='store_true', help='Exibe o(s) indivíduo(s) de fitness máximo ao final')
parser.add_argument('-meta ', '--metadata', action='store_true', help='Retorna, ao fim da execuçaõ, os metadados e parametors utilizados')
parser.add_argument('-s', '--seed', action='store_true', help='Adicionar seed manualmente')
parser.add_argument('-sv', '--seed_value', type=int, help='Valor da seed')
parser.add_argument('-tl', '--time_limit', type=float, help='Limite de tempo')
parser.add_argument('-div', '--divide', type=int, help='Divisão da população')
parser.add_argument('-m', '--mutation', type=float, help='Taxa de mutação')
parser.add_argument('-pop', '--population', type=int, help='Tamanho população')
parser.add_argument('-gen', '--max_gen', type=int, help='Quantidade de gerações')

#Adicionar opcao -m que printa os metadados utilizados (tamanho populacao, geracoes, eltitimos, seed utilizada no programa, etc)
#adiciona opcao -s que utiliza uma seed passada por argumento 
args = parser.parse_args()

# Checa se criterios de convergencia estão corretos
if args.seed:
    if args.seed is None:
            parser.error("Ao usar -s/--seed, você deve informar -sv e indicar o valor da seed")
    else:
        print(f'Used seed: {args.seed_value}')
        exec_seed = args.seed_value
else:
    exec_seed = random.randrange(sys.maxsize)

random.seed(exec_seed)

if args.mutation:
    mutation_rate = args.mutation 

if args.population: 
    population_size = args.population

if args.max_gen:
    num_generations = args.max_gen

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

if args.divide:
    if (args.divide <= 1):
        print("ERROR: divide must be at least 2")
    elif (gene_size // args.divide) < 2:
        print("ERROR: gene_size // divide must be at least 2")
        exit(0)
    pop_division = args.divide
else:
    pop_division = 1

generations_metadata = []
for i in range(pop_division):
    generations_metadata.append([])

gene_pop = []
for i in range(pop_division):
    gene_pop.append(gene_size // pop_division)

print("Scheduling session aggregation:")
print(scheduling_sesssions)
print("")


#population = gs.initial_population_random(scheduling_sesssions.copy(), user_nts_constraint.copy(), gene_size, population_size, nts, nu)
population = []
population_copy = []
start = 0

for i in range(pop_division):
    end = start + gene_pop[i]

    p = gs.initial_population_replicated_gene(scheduling_sesssions.copy()[start:end], user_nts_constraint.copy(), gene_pop[i], population_size, nts, nu)
    population.append(p)
    population_copy.append(p.copy())

    start = end

# print("Initial Population:")
# gs.print_population(population, population_size, gene_size,  nts)
# print("")

print("Crossover using Roulette, Timeslot Mutation and One-Point Crossover")
print(f"    Total Generations   : {num_generations}")
print(f"    Num. of Populations : {pop_division}")
print(f"    Population Size     : {population_size}")
print(f"    Mutation rate       : {mutation_rate}")
last_convergence = 0
conv_count = 0
start_time = time.perf_counter()

if (args.plot):
    for i in range(pop_division):
        gs.collect_generation_metadata(generations_metadata[i], population[i], population_size)

new_population = []
for i in range(pop_division):
    new_population.append(population[i])

if args.time_limit == None:
    for gen in range(num_generations):
        r = random.uniform(0, 1)
        if(r < crossover_rate):
            for i in range(pop_division):
                new_population[i] = gs.crossover(population[i], elitism_rate, tournament_size, gene_pop[i], population_size, nts, "roulette", "one-point", "renewall")  

        start = 0
        for i in range(pop_division):
            end = start + gene_pop[i]
            new_population[i] = gs.timeslot_mutation(new_population[i], scheduling_sesssions[start:end], mutation_rate, gene_pop[i], population_size, nts)
            start = end

        if (args.plot) or (gen == num_generations-1): 
            for i in range(pop_division):
                gs.collect_generation_metadata(generations_metadata[i], new_population[i], population_size)

        for i in range(pop_division):
            population[i] = new_population[i].copy()
else:
    gen = 0
    while(True):
        r = random.uniform(0, 1)
        if(r < crossover_rate):
            for i in range(pop_division):
                new_population[i] = gs.crossover(population[i], elitism_rate, tournament_size, gene_pop[i], population_size, nts, "roulette", "one-point", "renewall")  

        start = 0
        for i in range(pop_division):
            end = start + gene_pop[i]
            new_population[i] = gs.timeslot_mutation(new_population[i], scheduling_sesssions[start:end], mutation_rate, gene_pop[i], population_size, nts)
            start = end

        if (args.plot) or (gen == num_generations-1): 
            for i in range(pop_division):
                gs.collect_generation_metadata(generations_metadata[i], new_population[i], population_size)

        for i in range(pop_division):
            population[i] = new_population[i].copy()
        gen += 1

        elapsed_time  = time.perf_counter() - start_time
        if elapsed_time >= args.time_limit:
            for i in range(pop_division):
                gs.collect_generation_metadata(generations_metadata[i], new_population[i], population_size)
            break

end_time = time.perf_counter() - start_time

for i in range(pop_division):
    if(not gs.validate_scheduling(generations_metadata[0]['max_ind'][i][0], user_nts_constraint,nts, nu)):
        print(f"Erro: scheduling {i} é inválido: ")
        print(generations_metadata[0]['max_ind'][i][0])
        exit(1)

print("Scheduling final válido!")

max_fitness = 0.0
if args.plot:
    for j in range(pop_division):
        max_fitness += generations_metadata[j][gen]['max']
else:
    for j in range(pop_division):
        max_fitness += generations_metadata[j][0]['max']

if args.plot:
    print(f"Max fitness of generation {gen+1} = {max_fitness:.2f} found in {end_time:.2f} secs")
    with open("metadata.txt", "w") as metadataFile:
        for k in range(gen):
            low_f = 0.0
            avg_f = 0.0
            max_f = 0.0
            for j in range(pop_division):
                low_f += generations_metadata[j][k]['low']
                avg_f += generations_metadata[j][k]['avg']
                max_f += generations_metadata[j][k]['max']
            metadataFile.write(f"{low_f:.2f} - {avg_f:.2f} - {max_f:.2f}\n")
else:
    print(f"Max fitness of generation {gen+1} = {max_fitness:.2f} found in {end_time:.2f} secs")

# print("Final Population:")
# gs.print_population(new_population, population_size, gene_size,  nts)
# print("")

if args.finalind:
    maxIndvs = []

    print("Maximal individuals:")
    for ind in range(population_size):
        # reconstrói indivíduo completo
        full_individual = []

        for p_ind in range(pop_division):
            full_individual.extend(population[p_ind][ind])

        full_individual = np.array(full_individual)
        nao_pertence = not any(np.array_equal(full_individual, x) for x in maxIndvs)
        is_max = np.isclose(gs.fitness(full_individual), max_fitness)
        
        if is_max and nao_pertence:
            maxIndvs.append(full_individual)
            print("\t", end="")
            for j in range(gene_size):
                print(f"{full_individual[j][0]}", end="")

            print("")

if args.plot:
    cPlot.plotFitness()

if args.metadata:
    print("\n")
    print("---- Metadata and Parameters -----")
    print(f"    Seed: {exec_seed}")
    print(f"    Population size: {population_size}")
    print(f"    Num. of Populations: {pop_division}")
    print(f"    Generation Number: {num_generations}")
    print(f"    Elitism Rate: {elitism_rate:.2f}")
    print(f"    Mutation Rate: {mutation_rate:.2f}")
    print(f"    Tournament Size: {tournament_size}")
 