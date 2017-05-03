#!/bin/bash
start=5
end=200
step=5

for((i=start; i<=end; i=i+step))
do
  ./network_gen.py $i $i $i $i

done
