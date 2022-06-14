#!/bin/bash

for file in benchmark_dat/*;
do
 f1=${file#"benchmark_dat/"}
 f=${f1%".dat"}
 echo $f
 ./runLP.sh $f;
done
