import numpy as np 
import random as rand


def create_scheduling_mask(scheduling_sessions, usage_constraint, gene_size, nts, nu):
    scheduling_mask = []
    for j in range (0, gene_size): 
        usage_constraint_counter = usage_constraint.copy()
        for k in range(0, nts):
            user = rand.randint(0, nu - 1)
            while (usage_constraint_counter[user] == 0):
                user = rand.randint(0, nu - 1)
            scheduling_mask.append(user)
    
    return scheduling_mask


def initial_population_replicated_gene(scheduling_sessions, usage_constraint, gene_size, population_size, nts, nu):

    population = []
    for _ in range(0, population_size):
        individual = []

        scheduling_mask = create_scheduling_mask(scheduling_sessions, usage_constraint, gene_size, nts, nu)
        for j in range (0, gene_size): 
            gene = []
            schedule = np.empty((2, nts))
            for k in range(0, nts):
                #print(f'{j} , {k}, {user}')
                user = scheduling_mask[k]
                schedule[0][k] = user
                schedule[1][k] = scheduling_sessions[j][user][k] 
            
            gene.append(schedule)

            individual.append(gene)

        population.append(individual)        

    return np.array(population)


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


def roulette_selection(fitness_values):
    return rand.choices(range(len(fitness_values)), weights=fitness_values, k=1)[0]


def tournament_selection(population, fitness_values, tournament_size):
    indices = rand.sample(range(len(population)), tournament_size)
    return max(indices, key=lambda i: fitness_values[i])


def crossover(population, elitism_rate, tournament_size, gene_size, population_size, dna, selection_type, crossover_type, child_selection):
    fitness_values = [fitness(ind) for ind in population]

    elite_size = int(elitism_rate * population_size)
    elite = sorted(zip(population, fitness_values), key=lambda x: x[1], reverse=True)

    new_population = [ind for ind, _ in elite][:elite_size]
    
    del elite[:elite_size]

    if(child_selection == "weak_substitution"):
        sorted_population = sorted(elite, key=lambda x: x[1], reverse=False)

    # Gera novos individuos mantendo o tamanho da população inicial
    for _ in range(0, population_size-elite_size):
        if selection_type == "random":
            a = rand.randint(0, population_size-1)
            b = rand.randint(0, population_size-1)

        elif selection_type == "roulette":
            a = roulette_selection(fitness_values)
            b = roulette_selection(fitness_values)

        elif selection_type == "tournament":
            a = tournament_selection(population, fitness_values, tournament_size)
            b = tournament_selection(population, fitness_values, tournament_size)

        if(crossover_type == "uniform"):
            child = uniform_crossover(a, b, population, gene_size)
        elif(crossover_type == "one-point"):
            child = one_point_crossover(a, b, population, gene_size)
        elif(crossover_type == "two-point"):
            child = two_point_crossover(a, b, population, gene_size)
        elif(crossover_type == "dominant"):
            child = dominant_crossover(a, b, population, gene_size)


        if(child_selection == "renewall"):
            new_population.append(child)

        elif(child_selection == "parent_substitution"):

            fit_a = fitness_values[a]
            fit_b = fitness_values[b]
            fit_child = fitness(child)

            if(fit_child >= fit_a and fit_child >= fit_b):
                new_population.append(child)
            elif(fit_a >= fit_b):
                new_population.append(population[a])
            else:
                new_population.append(population[b])

        elif(child_selection == "weak_substitution"): 

            if(len(sorted_population) == 0):
                new_population.append(child)
            else: 
                fit_child = fitness(child)

                if(fit_child >= sorted_population[0][1]):
                    new_population.append(child)
                    sorted_population.pop(0)
                else:
                    new_population.append(sorted_population[0][0])

    return np.array(new_population)


def gene_fitness(gene):
    return np.sum([dna[0][1] for dna in gene])


def dominant_crossover(a, b, population, gene_size):
    
    child = []

    for i in range(0, gene_size):
        gene_a = population[a][i]
        gene_b = population[b][i]

        gene_fitness_a = gene_fitness(gene_a)
        gene_fitness_b = gene_fitness(gene_b)

        if(gene_fitness_a > gene_fitness_b):
            child.append(gene_a)
        else: 
            child.append(gene_b)
    
    return child

def uniform_crossover(a, b, population, gene_size):
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
    
    return child


def one_point_crossover(a, b, population, gene_size):
    child1 = []
    child2 = []

    crossover_point = rand.randint(0, gene_size-1)

    mask1 = [0]*gene_size
    mask2 = [1]*gene_size

    for i in range(crossover_point, gene_size):
        mask1[i] = 1
        mask2[i] = 0
    
    for i in range(0, gene_size):
        gene_child1 = a if mask1[i] == 0 else b
        gene_child2 = a if mask2[i] == 0 else b

        child1.append(population[gene_child1][i])
        child2.append(population[gene_child2][i])

    fitness_child1 = fitness(child1)
    fitness_child2 = fitness(child2)

    if(fitness_child1 >= fitness_child2):
        return child1
    
    return child2


def two_point_crossover(a, b, population, gene_size):
    child1 = []
    child2 = []

    crossover_point_1 = rand.randint(0, gene_size-1)
    crossover_point_2 = rand.randint(crossover_point_1, gene_size-1)

    mask1 = [0]*gene_size
    mask2 = [1]*gene_size


    for i in range(crossover_point_1, crossover_point_2):
        mask1[i] = 1
        mask2[i] = 0
    
    for i in range(0, gene_size):
        gene_child1 = a if mask1[i] == 0 else b
        gene_child2 = a if mask2[i] == 0 else b

        child1.append(population[gene_child1][i])
        child2.append(population[gene_child2][i])

    fitness_child1 = fitness(child1)
    fitness_child2 = fitness(child2)

    if(fitness_child1 >= fitness_child2):
        return child1
    
    return child2

# Calcula fitness somando os User Rates a cada timeslot
def fitness(individual):
    return np.sum([gene[0][1] for gene in individual])


# Mutação que ocorre trocando duas sessões de lugar
def session_mutation(population, scheduling_sessions, mutation_rate, gene_size, population_size, dna):
    new_population = population.copy()

    random_values = [rand.random() for _ in range(population_size)]

    for i in range(population_size):
        if random_values[i] < mutation_rate:

            a, b = rand.sample(range(gene_size), 2)

            ind = new_population[i]

            sess_a = ind[a][0]
            sess_b = ind[b][0]

            genes_a = sess_a[0]
            genes_b = sess_b[0]

            # swap genes
            sess_a[0], sess_b[0] = genes_b.copy(), genes_a.copy()

            # atualizar rates (vetorizado)
            idx = np.arange(dna)

            sess_a[1] = scheduling_sessions[a][sess_a[0].astype(int), idx]
            sess_b[1] = scheduling_sessions[b][sess_b[0].astype(int), idx]

    return np.array(new_population)


# Mutação que ocorre trocando duas timeslots de uma seção de lugar
def timeslot_mutation(population, scheduling_sessions, mutation_rate, gene_size, population_size, dna):
    new_population = population.copy()

    for i in range(population_size):
        r = rand.uniform(0, 1)
        if r < mutation_rate:
            mutation_swap_timeslot(new_population[i], scheduling_sessions,  gene_size, dna) 

    return np.array(new_population)



# def mutation_operator(population, population_size, gene_size, predicted_rates, dna, mutation_type):

#     index = rand.randint(0,population_size -1)
#     individual = population[index]

#     mutation_type(individual, predicted_rates, gene_size, dna)

#     return index


def mutation_swap_timeslot(individual, predicted_rates, gene_size, dna):

    for i in range(0, gene_size):

        
        timeslot_a = rand.randint(0, dna - 1)
        timeslot_b = rand.randint(0, dna - 1)
        while(timeslot_a == timeslot_b ):
            timeslot_b = rand.randint(0, dna - 1)

        user_a = int(individual[i][0][0][timeslot_a])
        user_b = int(individual[i][0][0][timeslot_b])


        new_rate_a = predicted_rates[i][user_a][timeslot_b]
        new_rate_b = predicted_rates[i][user_b][timeslot_a]
        #print( individual[i][0])
        #print(f'    gene: {i} | ta: {timeslot_a} | tb: {timeslot_b}')
        #print(f'    {user_a} and {user_b}')
        #print(f'    a: {predicted_rates[i][user_a][timeslot_a]} b:{predicted_rates[i][user_b][timeslot_b]}')

        individual[i][0][0][timeslot_a] = user_b
        individual[i][0][1][timeslot_a] = new_rate_b

        individual[i][0][0][timeslot_b] = user_a
        individual[i][0][1][timeslot_b] = new_rate_a

    return 

def collect_generation_metadata(generation_metadata, population, population_size):
        
    max_fit = 0.0
    avarege_fit = 0.0
    lowest_fit = 1e10
    for j in range(population_size):
        f = fitness(population[j])

        avarege_fit += f
        
        if f > max_fit:
            max_fit = f
        if f < lowest_fit:
            lowest_fit = f 

    avarege_fit /= population_size

    gen_metadata = {"max": max_fit, "low": lowest_fit, "avg": avarege_fit}
    generation_metadata.append(gen_metadata)


def print_generation_metadata(generation_metadata, num_generations):

    for i in range(num_generations):
        gen_meta = generation_metadata[i]
        print(f"gen-{i}:")
        print_one_generation(gen_meta)


def print_one_generation(gen_meta):
    print(f"    max     fitness:{gen_meta['max']:.2f}")
    print(f"    average fitness:{gen_meta['avg']:.2f}")
    print(f"    lowest  fitness:{gen_meta['low']:.2f}")
    print("-" * 10) 


def check_convergence(generation_metadata, current_generation, convergence_analysis, threshold, last_convergence):
    count = 0

    if(convergence_analysis > current_generation) or (current_generation < last_convergence+convergence_analysis):
        return 0
    
    convergence_analysis_point = current_generation - convergence_analysis

    for i in range(convergence_analysis_point, current_generation):
        avg_fitness = generation_metadata[i]["avg"]
        max_fitness = generation_metadata[i]["max"]
        diff = max_fitness - avg_fitness

        if(diff < threshold):
            count += 1

    if(count == convergence_analysis):
        return 1 

    return 0

def hypermutation(population, scheduling_sessions, usage_constraint, gene_size, population_size, nts, nu, discarded_percent):
    discarded_size = int(population_size * discarded_percent)

    # Calcula fitness direto em array numpy (sem dict)
    fitness_values = np.array([fitness(ind) for ind in population])

    # Pega índices ordenados (menor fitness primeiro)
    sorted_idx = np.argsort(fitness_values)

    # Mantém apenas os melhores (metade superior)
    survivors = population[sorted_idx[discarded_size:]]

    # Gera novos indivíduos (só o necessário!)
    #new_individuals = initial_population_random(scheduling_sessions, usage_constraint, gene_size, discarded_size, nts, nu)
    new_individuals = initial_population_replicated_gene(scheduling_sessions, usage_constraint, gene_size, discarded_size, nts, nu)

    # Junta tudo
    new_population = np.vstack((survivors, new_individuals))

    return new_population
