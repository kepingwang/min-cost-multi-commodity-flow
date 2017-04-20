#!/usr/bin/python
#This is a test script for the algorithm
import sys
from greedy import Network
network=Network()
#unit test1 : read 
network.readGraph(sys.argv[1])
network.printGraph()
#unit test 2: queryPath
network.queryPath(network.requirements)
