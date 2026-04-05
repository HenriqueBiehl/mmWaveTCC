# BILP Solver

## 1. Requisitos 🛠️
- IBM ILOG CPLEX Optimization Studio
- Python 3.x
- `BILP.dat` preenchido
- `BILP.mod` preenchido

### 1.1 Instalando o IBM COS *NO LINUX* 🐧
- Crie uma conta em [https://www.ibm.com/br-pt](https://www.ibm.com/br-pt) e faça login na página
- Acesse [esse](https://www.ibm.com/br-pt/products/ilog-cplex-optimization-studio) link e clique em "Experimente sem custo"
- Na dashboard, na parte de Downloads, procure pelo IBM ILOG CPLEX Optimization Studio Free Edition e clique em "Download"
- Na página da Box@IBM, escolha a versão a versão de Linux para baixar
- Após o Download, dê permissão de execução ao arquivo .bin com `chmod +x cos_installer_preview-x.x.x-linux-x86-64.bin`
- Execute o arquivo pelo terminal com `./cos_installer_preview-x.x.x-linux-x86-64.bin`
- Siga as instruções de instalação, SEM ALTERAR O LOCAL PADRÃO DE INSTALAÇÃO (`/opt/ibm/ILOG/CPLEX_Studio_Community2212/`)

## 2. Arquivos 📁
- `EntradaBILP.py`: Executável Python que converte os dados de entrada para um formato aceito pelo Solver do BILP
- `BILP.mod`: Arquivo em OPL (Optimization Programming Language) descrevendo as variáveis contidas na execução do BILP, função objetivo, restrições e saída do programa
- `BILP.dat`: Arquivo com os dados referentes ao BILP, como os vetores, matriz A, e variáveis para execução do programa
- `BILP.py`: Executável Python que vai verificar a existência do IBM CPLEX e dos arquivos acima e depois rodar o Otimizador com os dados referenciados, gerando um arquivo de saída `output.txt`
- `randomSessionGenerator.py`: Executável Python que gera um arquivo de sessão distância e atenuação aleatórias para cada usuário dados um número de timeslots, número de usuários, atenuação máxima e distância máxima entre UE-AP

## 3. Execução ⏯️
- Execute o arquivo `EntradaBILP.py` e depois dando uma entrada válida ou redirecionando de um arquivo de entrada (`python3 EntradaBILP.py < entrada/session-1.txt`), que gerará um novo `BILP.dat`
- Execute o arquivo `BILP.py` pela linha de comando (`python3 BILP.py`) e agurade a execução do *solver*

## 4. Por que não usar a IDE do OPL? 🤔
- Interface desnecessária que apenas consumiria tempo e recursos do sistema, considerando que temos uma alternativa na linha de comando
- Complicado de controlar como se comporta em diferentes sistemas
- Mais difícil de controlar pelo Git