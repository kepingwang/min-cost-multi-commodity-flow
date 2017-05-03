#!/bin/bash
start=5
end=200
step=5

for((i=start; i<=end; i=i+step))
do
python ./greedytest.py graph/$i.net |tee out.txt|tee out/$i.out
done
