#!/bin/bash
for ((j=1;j<6;j+=1))
do
    for ((i=100;i<4000;i+=100))
    do
	python resolver.py $i $j
	awk -v fname=$i '/returned/{sum+=$9}END{print fname, sum}' bind.log
	mv bind.log trials$j/bind.log$i
    done
    mv k_hist trials$j/
done