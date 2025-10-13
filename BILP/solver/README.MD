# BILP Solver Runner

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
- `BILP.mod`: Arquivo em OPL (Optimization Programming Language) descrevendo as variáveis contidas na execução do BILP, função objetivo, restrições e saída do programa
- `BILP.dat`: Arquivo com os dados referentes ao BILP, como os vetores, matriz A, e variáveis para execução do programa
- `runner.py`: Executável Python que vai verificar a existência do IBM CPLEX e dos arquivos acima e depois rodar o Otimizador com os dados referenciados, gerando um arquivo de saída `output.txt`

## 3. Execução ⏯️
Apenas invoque o arquivo Python pela linha de comando (`./runner.py`) e agurade a execução do *solver*

## 4. Por que não usar a IDE do OPL? 🤔
- Interface desnecessária que apenas consumiria tempo e recursos do sistema, considerando que temos uma alternativa na linha de comando
- Complicado de controlar como se comporta em diferentes sistemas
- Mais difícil de controlar pelo Git