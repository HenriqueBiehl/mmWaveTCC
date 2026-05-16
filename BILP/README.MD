# Algoritmo Ótimo de Escalonamento em Redes mmWave

## 📝 Projeto
Este projeto se trata de um algoritmo ótimo para encontrar o escalonamento de uma rede mmWave seguindo restrições de fairness.

## 🛠️ Requisitos 
- IBM ILOG CPLEX Optimization Studio
- Python 3.x
- `BILP.dat` preenchido
- `BILP.mod` preenchido

### 🐧 Instalando o IBM COS *NO LINUX* 
- Crie uma conta em [https://www.ibm.com/br-pt](https://www.ibm.com/br-pt) e faça login na página
- Acesse [esse](https://www.ibm.com/br-pt/products/ilog-cplex-optimization-studio) link e clique em "Experimente sem custo"
- Na dashboard, na parte de Downloads, procure pelo IBM ILOG CPLEX Optimization Studio Free Edition e clique em "Download"
- Na página da Box@IBM, escolha a versão a versão de Linux para baixar
- Após o Download, dê permissão de execução ao arquivo .bin com `chmod +x cos_installer_preview-x.x.x-linux-x86-64.bin`
- Execute o arquivo pelo terminal com `./cos_installer_preview-x.x.x-linux-x86-64.bin`
- Siga as instruções de instalação, SEM ALTERAR O LOCAL PADRÃO DE INSTALAÇÃO (`/opt/ibm/ILOG/CPLEX_Studio_Community2212/`)

### 🤔 Por que não usar a IDE do OPL? 
- Interface desnecessária que apenas consumiria tempo e recursos do sistema, considerando que temos uma alternativa na linha de comando
- Complicado de controlar como se comporta em diferentes sistemas
- Mais difícil de controlar pelo Git

## 📁 Pastas
- **entrada**: Entradas de teste para o programa, sendo cada conjunto de sessões organizado em subpastas

## 📑 Arquivos 
- `EntradaBILP.py`: Executável Python que converte os dados de entrada para um formato aceito pelo Solver do BILP
- `BILP.mod`: Arquivo em OPL (Optimization Programming Language) descrevendo as variáveis contidas na execução do BILP, função objetivo, restrições e saída do programa
- `BILP.dat`: Arquivo com os dados referentes ao BILP, como os vetores, Nu, Nts e variáveis para execução do programa
- `BILP.py`: Executável Python que vai verificar a existência do IBM CPLEX e dos arquivos acima e depois rodar o Otimizador com os dados referenciados, gerando um arquivo de saída `output.txt`
  - **Uso**: execute *BILP.py* e aguarde o resultado na tela.
  - **Opções:**:
    - `-d <dir>`: Executa o BILP para todos as entradas de certo diretório
    - `-f <file>`: Executa o BILP com uma entrada específica
    - `-x`: Mostra na saída o vetor com a resposta final do BILP
- `randomSessionGenerator.py`: Executável Python que gera um arquivo de sessão com dados aleatórios dado um range máximo e um mínimo de rate dos usuários.
    - **Uso**: apenas executar *randomSessionGenerator.py* e inserir os dados requeridos. O resultado será salvo em BILP.dat
- `run_tests.sh`: Roda o programa 30x e relata as médias de tempo e de *bandwidth* das execuções