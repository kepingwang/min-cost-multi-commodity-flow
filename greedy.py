#!/usr/bin/python
import sys
import copy
from edge import Edge
from sets import Set
from min_cost_flow import MinCostFlow
arglenth=len(sys.argv)
class greedyMCMC:
    def __init__(self, pnumvertices=0):
        self.numV=pnumvertices
        #edgelist
        self.original_edges=[]
        self.edges=[]
        #self.balls=[]
        self.exclusivePaths=[]
        self.edgeid=0
        self.requirements=[]
        self.alledges=[]
        self.maxCost=0
        self.maxCapacity=0
    def printGraph(self):
        print "-------GRAPH----------"
        print "num of vertices: "+str(self.numV)
        print "edges:"
        for e in self.edges:
            for e1 in e:
                print str(e1)
        for r in self.requirements:
            print r
    def readGraph(self,filename):
        f=open(filename)
        self.numV=int(f.readline().replace("\n",""))
        for i in range(self.numV):
            adjedge=[]
            self.edges.append(adjedge)
        line=f.readline().replace("\n","")
        mode=0
        while(line!=""):
            if(line.startswith("#")):
                line=f.readline()
                continue
            if line.find("req")!=-1:
                mode=1
                line=f.readline()
                continue
            if mode==0:
                edge=line.split(" ")
                self.addEdge(int(edge[0]),int(edge[1]),int(edge[2]),int(edge[3]))
            else:
                edge=line.split(" ")
                self.addRequirement(int(edge[0]),int(edge[1]),int(edge[2]))
            line=f.readline()
        self.original_edges=copy.deepcopy(self.edges)

    def addRequirement(self,v1,v2,b):
        self.requirements.append([v1,v2,b])
    def addEdge(self,v1,v2,capacity,cost):
        edgelist=self.edges[v1]
        newedge=Edge(self.edgeid,v1,v2,capacity,cost)
        self.alledges.append(newedge)
        for e in edgelist:
            if e.v1==v1 and e.v2==v2:
                print "edge already exists ! please check"
        edgelist.append(newedge)
        self.edges[v1]=edgelist
        edgelist=self.edges[v2]
        for e in edgelist:
            if e.v1==v1 and e.v2==v2:
                print "edge already exists! please check"
        edgelist.append(newedge)
        self.edges[v2]=edgelist
    #input:[[v_i1,v_i2,b_i]]
    def greedy(self, listofpairs):
      print "len(listofpairs): %s" %(len(listofpairs))
      sop=Set()
      for p in listofpairs:
        sop.add((p[0],p[1]))
      print "len(setofpairs): %s" %(len(sop))
      
      solutions={}
      e_pair={}
      ITER=10000
      cur=0
      while(len(solutions)<len(listofpairs)):
        for pair in listofpairs:
          print "%s < %s"%(len(solutions),len(listofpairs))
          cur+=1
          print cur
          #sys.stdout.flush()
          if (pair[0],pair[1]) in solutions:
            continue
          #print "hah"
          flow=MinCostFlow.minCostFlow(pair[0],pair[1],pair[2],self.alledges,False)
          #print "Flow1"
          #self.printFlow(flow)
          if len(flow)>0:
            for link in flow:
              solutions[(pair[0],pair[1])]=flow
              link[0].useBW(link[1])
              #self.printGraph()
              if link[0] in e_pair:
                s=e_pair[link[0]]
                s.add((pair[0],pair[1]))
              else:
                s=Set()
                s.add((pair[0],pair[1]))
                e_pair[link[0]]=s
          else:
            newflow=MinCostFlow.minCostFlow(pair[0],pair[1],pair[2],self.alledges,True)
            #print "Flow2"
            #self.printFlow(newflow)
            for link in newflow:
              if link[0].getAVLBW()<link[1]:
                link[0].extendBeta(1)
                for p in e_pair[link[0]]:
                  sol=solutions.pop(p)
                  for ec in sol:
                    ec[0].avlBW+=ec[1]
                    if ec[0]!=link[0]:
                      e_pair[ec[0]].remove(p)
                e_pair[link[0]]=Set()
      for pair in solutions:
        print str(pair)
        sol=solutions[pair]
        self.printFlow(sol)
      if len(solutions)==len(listofpairs):
        print "success after %s iterations" %(cur)
        print "number of edges: %s"%(len(self.alledges))
        print "number of requests:%s " %(len(listofpairs))
        print "number of vertices:%s " %(self.numV)
        usedbw=self.usedBW(solutions)
        cost = sum([k.cost*usedbw[k] for k in usedbw])
        print "total cost %s"%(cost)
        print "maximum capacity %s"%(self.maxCapacity)
      else:
        print "fail after %s iterations" %(cur)

    def usedBW(self,x):
      usedbw={}
      for flow in x:
        for link in x[flow]:
          if(link[0] in usedbw):
            usedbw[link[0]]=usedbw[link[0]]+link[1]
          else:
            usedbw[link[0]]=link[1]
      return usedbw

    def printFlow(self,flow):
        for link in flow:
          print "edge: %s [%s]"%(link[0],link[1])

