#!/bin/bash
python ./test.py graph/$1.net $2 $3 |tee out.txt|tee out/$1.out
