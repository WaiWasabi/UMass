#!/bin/bash 

cd tuningw

dir=$(ls -l . |awk '/^d/ {print $NF}')
for i in $dir
do
cd $i
cd ../$i
bsub < bsub.sh
done
