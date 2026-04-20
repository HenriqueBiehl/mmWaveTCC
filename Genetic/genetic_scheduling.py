import numpy as np 
import random as rand

def initial_population_random(scheduling_sessions, usage_constraint, gene_size, population_size, nts, nu):
    
    population = []
    for _ in range(0, population_size):
        individual = []

        for j in range (0, gene_size): 
            usage_constraint_counter = usage_constraint.copy()
            gene = []
            schedule = np.empty((2, nts))
            for k in range(0, nts):
                user = rand.randint(0, nu - 1)
                while (usage_constraint_counter[user] == 0):
                    user = rand.randint(0, nu - 1)
                usage_constraint_counter[user] -= 1

                #print(f'{j} , {k}, {user}')
                schedule[0][k] = user
                schedule[1][k] = scheduling_sessions[j][user][k] 
            
            gene.append(schedule)

            individual.append(gene)


        population.append(individual)        

    return np.array(population)


def print_population(population, population_size, gene_size, dna):

    for i in range(0, population_size):
        print(f'ind{i}:')
        
        print_individual(population[i], gene_size, dna)
        
        print("")

def print_individual(individual, gene_size, dna):

    for j in range(0, gene_size):
    
        for k in range (0, dna):
            print(f'{int(individual[j][0][0][k]): >4} |', end="")
        print("")
        for k in range (0, dna):
            print(f'{individual[j][0][1][k]:.2f} |', end="")

        print("")


def roulette_selection(population, population_size, gene_size, dna):
    total_fitness = 0.0
    for p in population:
        total_fitness += fitness(p, gene_size, dna)
    
    spin = rand.uniform(0, total_fitness)
    cumulative = 0.0

    for i in range(population_size):
        cumulative += fitness(population[i], gene_size, dna)
        if spin < cumulative:
            return i


def crossover(population, elitism_rate, gene_size, population_size, dna, selection_type):
    from operator import itemgetter

    new_population = []

    # Elitismo seleciona elitism_rate% da população para continuar igual na proxima geracao
    elite_size = int(elitism_rate * population_size)
    fitness_values = []
    for i in range(0, population_size):
        fitness_values.append({"pos": i, "fitness": fitness(population[i], gene_size, dna)})
    fitness_values.sort(key=itemgetter('fitness'))
    fitness_values.reverse()
    elite = fitness_values[:elite_size]

    for e in elite:
        new_population.append(population[e["pos"]])

    # Gera novos individuos mantendo o tamanho da população inicial
    for _ in range(0, population_size-elite_size):
        if selection_type == "random":
            a = rand.randint(0, population_size-1)
            b = rand.randint(0, population_size-1)

            while a == b:
                b = rand.randint(0, population_size-1)

        elif selection_type == "roulette":
            a = roulette_selection(population, population_size, gene_size, dna)
            b = roulette_selection(population, population_size, gene_size, dna)

            while a == b:
                b = roulette_selection(population, population_size, gene_size, dna)

        # print(f"Crossover {a} e {b}")
        
        a_gene_heritage = gene_size - 1
        b_gene_heritage = gene_size - 1
        
        child = []

        for i in range(0, gene_size):

            parent_gene = rand.randint(0,1)

            if(parent_gene == 0 and a_gene_heritage != 0):
                child.append(population[a][i])
                a_gene_heritage -= 1
            elif (b_gene_heritage != 0):
                child.append(population[b][i])
                b_gene_heritage -= 1 
            else:
                child.append(population[a][i])
                a_gene_heritage -= 1


        new_population.append(child)

    return np.array(new_population)

# Calcula fitness somando os User Rates a cada timeslot
def fitness(individual, gene_size, dna):
    f = 0.0
    for i in range(0, gene_size):
        for k in range (0, dna):
            f += individual[i][0][1][k]

    return f

# Mutação que ocorre trocando duas sessões de lugar
def session_mutation(population, scheduling_sessions, mutation_rate, gene_size, population_size, dna):
    new_population = population.copy()

    for i in range(population_size):
        r = rand.uniform(0, 1)
        if r < mutation_rate:
            # print(f'ind{i} mutates with {r}')

            # Sessoes A e B vão trocar de lugar
            a = rand.randrange(0, gene_size)
            b = rand.randrange(0, gene_size)
            while a == b:
                b = rand.randrange(0, gene_size)
            
            tmp = new_population[i][a][0][0].copy()
            new_population[i][a][0][0] = new_population[i][b][0][0].copy()
            new_population[i][b][0][0] = tmp

            # Encontra rates novas das sessões trocadas
            for j in range(dna):
                user_a = int(new_population[i][a][0][0][j])
                user_b = int(new_population[i][b][0][0][j])

                new_population[i][a][0][1][j] = scheduling_sessions[a][user_a][j]
                new_population[i][b][0][1][j] = scheduling_sessions[b][user_b][j]

    return np.array(new_population)

def mutation_operator(population, population_size, gene_size, predicted_rates, dna, mutation_type):

    index = rand.randint(0,population_size -1)
    individual = population[index]

    mutation_type(individual, predicted_rates, gene_size, dna)

    return index



def mutation_swap_timeslot(individual, predicted_rates, gene_size, dna):

    mutated_gene = rand.randint(0, gene_size - 1)

    timeslot_a = rand.randint(0, dna - 1)
    timeslot_b = rand.randint(0, dna - 1)
    while(timeslot_a == timeslot_b ):
        timeslot_b = rand.randint(0, dna - 1)

    user_a = int(individual[mutated_gene][0][0][timeslot_a])
    user_b = int(individual[mutated_gene][0][0][timeslot_b])


    new_rate_a = predicted_rates[mutated_gene][user_a][timeslot_b]
    new_rate_b = predicted_rates[mutated_gene][user_b][timeslot_a]
    #print( individual[mutated_gene][0])
    #print(f'    gene: {mutated_gene} | ta: {timeslot_a} | tb: {timeslot_b}')
    #print(f'    {user_a} and {user_b}')
    #print(f'    a: {predicted_rates[mutated_gene][user_a][timeslot_a]} b:{predicted_rates[mutated_gene][user_b][timeslot_b]}')

    individual[mutated_gene][0][0][timeslot_a] = user_b
    individual[mutated_gene][0][1][timeslot_a] = new_rate_b

    individual[mutated_gene][0][0][timeslot_b] = user_a
    individual[mutated_gene][0][1][timeslot_b] = new_rate_a

    return 





