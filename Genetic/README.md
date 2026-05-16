# Algoritmo Genético de Escalonamento em Redes mmWave

## 📝 Projeto
Este projeto se trata de um algoritmo bioinspirado para encontrar o escalonamento de uma rede mmWave seguindo restrições de fairness. Trata-se de um algoritmo genético projetado especificamente para esse problema.

## 📑 Organização do projeto
### 🗂️ Pastas
- **BILPCompEntries**: Entradas a serem comparadas com o equivalente no BILP
- **Entradas**: Entradas de teste para o algoritmo
- **Generator_In**: Entradas para o gerador aleatório de entradas
- **Generator_Out**: Saídas do gerador aleatório de entradas, destinadas a serem usadas como entrada do algoritmo genético
- **GS_Out**: Saídas do algoritmo genético

### 📰 Arquivos
- **createPlot.py**: Arquivo com a função que lê o arquivo metadata.txt gerado pelo algoritmo genético e cria um plot usando a `matplotlib` mostrando a evolução da fitness dos indivíduos em relação ao número de gerações passadas
- **entry_generator.py**: Script que lê dados da entrada padrão e gera a partir dela uma entrada para o algoritmo genético no formato correto
  - **Uso**: execute *entry_generator.py* e insira os dados requeridos.
- **genetic_scheduling.py**: Arquivo com as funções principais do algoritmo genético.
- **main.py**: Arquivo principal que executa o algoritmo genético em si.
  - **Uso**: execute *main.py* e aguarde o resultado na tela.
  - **Opções:**:
    - `-p`: Plota na tela o gráfico com a relação de fitness X gerações
    - `-fi`: Exibe junto com os resultados finais do algoritmo, o indivíduo de maior fitness da última geração
    - `-s -sv <seed_value>`: Usa como seed das funções aleatórias o `seed_value` passado como parâmetro
    - `-tl <time_limit>`: Executa o programa por `time_limit` segundos apenas e exibe o resultado alcançado nesse tempo
    - `-meta`: Retorna, ao fim da execução, os metadados e parâmetros utilizados
    - `-c -g <generations> -mc <max_conv> -t <threshold>`: Executa o programa com detecção de convergência, olhando para `generations` gerações passadas, com `threshold` como limite de diferença e para o algoritmo após `max_conv` convergências
-**modelagem.txt**: Arquivo explicando a modelagem da entrada e funcionamento do algoritmo principal
- **out.txt**: Saídas do algoritmo usadas para comparação e acompanhamento da evolução do projeto
- **tests.txt**: Saídas do algoritmo usadas para comparação e acompanhamento da evolução do projeto
- **run_tests.sh**: Roda o programa 30x e relata as médias de tempo e de *bandwidth* das execuções