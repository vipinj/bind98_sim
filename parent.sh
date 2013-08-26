#!/bin/bash

function run_m ()
{
	python resolver.py $1 
	awk -v fname=$1 '/returned/{sum+=$9}END{print fname, sum}' bind.log_$1 >> k_hist_$j
	mv bind.log_$1 trials$1/
}

for ((j=5;j<11;j+=1))
do
    mkdir trials$j
#    for ((i=500;i<4000;i+=500))
#    do
    time run_m $j
    mv k_hist_$j trials$j/
done
