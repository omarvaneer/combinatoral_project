FILE=$1  #!"h1"
ampl <(echo "
reset;
model sc_ilp.mod;
data ./benchmark_dat/${FILE}.dat;
option solver cplex;
solve;
display x;
")>./ILP_out/${FILE}_ilp.out


