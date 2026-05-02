import matplotlib.pyplot as plt

def plotFitness():
    minimos = []
    medios = []
    maximos = []

    with open('metadata.txt', 'r') as f:
        for linha in f:
            partes = linha.strip().split('-')
            min_val = float(partes[0])
            med_val = float(partes[1])
            max_val = float(partes[2])

            minimos.append(min_val)
            medios.append(med_val)
            maximos.append(max_val)

    # eixo x = tempo (iterações)
    x = range(len(minimos))

    plt.plot(x, minimos, label='Fitness Mínimo')
    plt.plot(x, medios, label='Fitness Médio')
    plt.plot(x, maximos, label='Fitness Máximo')

    plt.xlabel('Geração')
    plt.ylabel('Fitness')
    plt.title('Evolução do Fitness ao longo do tempo')
    plt.legend()
    plt.grid()

    plt.show()