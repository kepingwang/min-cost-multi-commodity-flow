#!/usr/bin/python
#This is a test script for the algorithm
import sys
import time
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
start = time.time()
sys.stdout.flush()
print "Trying to solve %s with %s-approximation and cost %s"%(sys.argv[1],sys.argv[2],sys.argv[3])
budget=int(sys.argv[3])
high=budget
low=0
b=high
epsilon=float(sys.argv[2])
x=fastmcmc.fastApproximation(fastmcmc.requirements,epsilon,b)
bestx=x
while(high-low>low*float(sys.argv[2])):
  print "high: %s low: %s"%(high,low)
  if x is None:
    low=b
  else:
    high=b
  b=(low+(high-low)/2)
  x=fastmcmc.fastApproximation(fastmcmc.requirements,epsilon,b)
  if x is not None and x[1]<bestx[1]:
    bestx=x

print "it took", time.time() - start, "seconds. cost:"+str(bestx[1])


#network=greedyMCMC()
##unit test1 : read 
#network.readGraph(sys.argv[1])
##network.printGraph()
##unit test 2: queryPath
#start = time.time()
#network.greedy(network.requirements)
#print "it took", time.time() - start, "seconds."
