#!/bin/bash
nv=100
nvstart=5
nvstep=5

python ./test.py graph/$1.net |tee out.txt
