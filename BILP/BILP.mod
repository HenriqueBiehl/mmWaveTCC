// bilp.mod
// Indices
int nu = ...; // número de usuarios
int nts = ...; // número timeslots

int m = nu+nts;
int n = nu*nts;

// Dados
range Rows = 1..m;
range Cols = 1..n;

int A[i in Rows][j in Cols] =
  // blocos
  (i <= nu && j > (i-1)*nts && j <= i*nts) ? 1 :

  // identidade replicada
  (i > nu && j == i-nu) ? 1 :
  (i > nu && sum(k in 0..nu-1) (j == i-nu + k*nts) >= 1) ? 1 :

  0;

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
main {
  thisOplModel.generate();

  cplex.solve();
  writeln("Objective = ", cplex.getObjValue())
  writeln("x = ", thisOplModel.x);
}