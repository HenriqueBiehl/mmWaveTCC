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

        for j in range(0, gene_size):
            
            for k in range (0, dna):
                print(f'{int(population[i][j][0][0][k]): >4} |', end="")
            print("")
            for k in range (0, dna):
                print(f'{population[i][j][0][1][k]:.2f} |', end="")

            print("")
        
        print("")


def crossover(population, gene_size, population_size):
    new_population = []
    
    for _ in range(0, population_size):

        a = rand.randint(0, population_size-1)
        b = rand.randint(0, population_size-1)

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
