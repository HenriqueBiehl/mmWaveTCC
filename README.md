# mmWave TCC

## 📝 Projeto
Este projeto se trata de algoritmos para resolver o problema de escalonamento de dispositivos em redes mmWave, usando diversos métodos e os comparando em relação a eficácia e eficiência.

## 📑 Organização do projeto
### 🗂️ Pastas
- **Articles**: Artigos usados como ponto base do projeto
- **BILP**: Solução ótima de escalonamento em mmWave usando Binary Integer Linear Programming
- **Genetic**: Solução bioinspirada de escalonmento em mmWave usando Algoritmos Genéticos
- **Heuristic**: Solução heurística de escalonmaneto em mmWave usando Algorimtos Gulosos adaptados
- **Greedy**: Solução heurística de escalonamento em mmWave usando Algoritmos Gulosos "puros"
- **Rates**: Gerador de entradas para os algoritmos com rates baseados na fórmula de Shannon

### 📰 Arquivos
- **BILPtoGenetic.py**: Script Python que converte entradas (diversas sessões) do BILP em um certo diretório para um entrada do Algoritmo Genético.
  - **Uso**: apenas executar _BILPtoGenetic.py_ e inserir o diretório com os arquivos a serem convertidos. O resultado será salvo em _convert_out.txt_
