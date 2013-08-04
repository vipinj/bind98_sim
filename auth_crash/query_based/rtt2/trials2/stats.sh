#!/bin/sh

for i in bind.log*;
do
t1=`grep 'query 1000 sent to' $i | cut -d"," -f1`
t2=`grep 'query 4999 sent to' $i | cut -d"," -f1`
diff=$(($t2-$t1))
echo ${i:11} $diff >> t
done
sort -n t > real_time
rm t
paste k_hist real_time | awk '{print $1, $2, $4}' > final_op
