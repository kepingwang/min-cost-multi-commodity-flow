#!/usr/bin/python
#This is a test script for the algorithm
import sys
from greedy import greedyMCMC
from fastapproximate import fastApproxMCMC
#network=greedyMCMC()
#unit test1 : read 
#network.readGraph(sys.argv[1])
#network.printGraph()
#unit test 2: queryPath
#network.queryPath(network.requirements)
fastmcmc=fastApproxMCMC()
fastmcmc.readGraph(sys.argv[1])
fastmcmc.printGraph()
fastmcmc.fastApproximization(fastmcmc.requirements,0.2,1000)

network=greedyMCMC()
#unit test1 : read 
network.readGraph(sys.argv[1])
#network.printGraph()
#unit test 2: queryPath
network.greedy(network.requirements)
