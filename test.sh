#!/bin/bash
python ./test.py graph/$1.net |tee out.txt|tee out/$1.out
