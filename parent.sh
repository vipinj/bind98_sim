#!/bin/bash

function run_m ()
{
	python resolver.py $1 $2 
	awk -v fname=$1 '/returned/{sum+=$9}END{print fname, sum}' bind.log_$2_$1 >> k_hist_$j
	mv bind.log_$2_$1 trials$2/
}

for ((j=5;j<11;j+=1))
do
    mkdir trials$j
    for ((i=500;i<4000;i+=500))
    do
	run_m $i $j
    done
    mv k_hist_$j trials$j/
done
