FILE=$1  #!"h1"
ampl <(echo "
reset;
model sc_lp.mod;
data ./benchmark_dat/${FILE}.dat;
option solver cplex;
solve;
display x;
")>./LP_out/${FILE}_lp.out