// bilp.mod
// Indices
int m = ...; // número de restrições (linhas de A)
int n = ...; // número de variáveis (colunas de A)

// Dados
int A[1..m][1..n] = ...; // matriz binária m x n
int B[1..m] = ...;       // vetor B (inteiro)
float R[1..n] = ...;     // vetor de coeficientes do objetivo

// Variáveis binárias
dvar boolean x[1..n];

// Objetivo
maximize sum(j in 1..n) R[j] * x[j];

// Restrições de igualdade AX = B
subject to {
  forall(i in 1..m)
    sum(j in 1..n) A[i][j] * x[j] == B[i];
}

// Impressão / saída
execute {
  writeln("Objective = ", cplex.getObjValue());
  writeln("x = ", x);
}