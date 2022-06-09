#Linear Programming Formulation

#one variable for each subset (N)
#one constraint for each element in true set (M) (sum of row is at least 1).
#minimize sum of variables

param M integer;
param N integer;

param matr {i in 0..M-1, j in 0..N-1} binary;

var x {j in 0..N-1};

maximize objective: -1 * sum {j in 0..N-1} x[j];
subject to C1 {i in 0..M-1}: sum{j in 0..N-1} matr[i,j] * x[j]>=1;
C2 {j in 0..N-1}: x[j] >= 0;
