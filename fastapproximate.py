#!/usr/bin/python
import math
import sys
import copy
from edge import Edge
from sets import Set
from min_cost_flow import MinCostFlow
arglenth=len(sys.argv)
class fastApproxMCMC:
    def __init__(self, pnumvertices=0):
        self.numV=pnumvertices
        #edgelist
        self.original_edges=[]
        self.edges=[]
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
    def fastApproximization(self, listofpairs,epsilon,budget):
      #Step1, compute a solution x, which maybe infeasible
      x=self.minX(listofpairs,self.alledges)
      #Step2, compute \lambda_0
      #for each edge, compute used bandwidth /capacity, find the minimum and maximum ratio
      #While max_i a_ix/b_i >= \lambda0/2 and x and y do not satisfy P2
        #For each i=1,...m: set y_i <--1/b_i e^(\alpha a_i x/b_i)
        #find a min-cost point x' \in P for cost c=y^t A
        #update x <-- (1-\sigma)x +\sigma x'
      usedbw=self.usedBW(x)
      m=len(self.alledges)
      lambda_0=self.maxRatio(usedbw,budget)
      alpha=4/lambda_0/epsilon*math.log(2*m/epsilon)
      totalflow=sum([r[2] for r in listofpairs])
      mincapacity=min(e.capacity for e in self.alledges)
      rou=float(totalflow)/float(mincapacity)
      sigma=epsilon/(4*alpha*rou)
      maxratio=lambda_0
      y=[]
      totalcost=sum([usedbw[k]*k.cost for k in usedbw])
      cost_y=1/float(budget)*math.exp(alpha*totalcost/budget)
      for i in range(m):
        if self.alledges[i] in usedbw:
          y.append(1/float(self.alledges[i].capacity)*math.exp(alpha*(float(usedbw[self.alledges[i]])/float(self.alledges[i].capacity))))
          self.alledges[i].beta=y[i]+cost_y*self.alledges[i].cost-self.alledges[i].cost

        else:
          y.append(1/float(self.alledges[i].capacity))
          self.alledges[i].beta=y[i]+cost_y*self.alledges[i].cost-self.alledges[i].cost
      y.append(cost_y)
      minx=self.minX(listofpairs,self.alledges)
      iterate=0
      while maxratio>=lambda_0/2 and not self.determineP2(usedbw,self.alledges,y,minx,epsilon,maxratio,budget):
        print "interation: %s"%(iterate)
        iterate+=1
        sys.stdout.flush()
        y=[]
#        for i in range(m):
#          self.alledges[i].cost=(1/float(self.alledges[i].capacity)*math.exp(alpha*(float(usedbw[self.alledges[i]])/float(self.alledges[i].capacity))))
        totalcost=sum([usedbw[k]*k.cost for k in usedbw])
        cost_y=1/float(budget)*math.exp(alpha*totalcost/budget)
        for i in range(len(self.alledges)):
          e=self.alledges[i]
          if self.alledges[i] in usedbw:
            y.append(1/float(e.capacity)*math.exp(alpha*(float(usedbw[e])/float(e.capacity))))
            self.alledges[i].beta=y[i]+cost_y*self.alledges[i].cost-self.alledges[i].cost
          else:
            y.append(1/float(e.capacity))
            self.alledges[i].beta=y[i]+cost_y*self.alledges[i].cost-self.alledges[i].cost
        y.append(cost_y)

        minx=self.minX(listofpairs,self.alledges)
        #update x
        new_x=[]
        for j in range(len(x)):
          newflow={}
          f_old=x[j]
          for link in f_old:
            newflow[link[0]]=(1-sigma)*link[1]
          f_new=minx[j]
          for link in f_new:
            if link[0] in newflow:
              newflow[link[0]]+=sigma*link[1]
            else:
              newflow[link[0]]=sigma*link[1]
          nf=[[k,newflow[k]] for k in newflow]
          new_x.append(nf)
        x=new_x
        print "sol x"
        for flow in x:
          self.printFlow(flow)
        usedbw=self.usedBW(x)
        maxratio=self.maxRatio(usedbw,budget)
      if maxratio>1+epsilon:
        print "No feasible solution with approximation"
      else:
        for flow in x:
          self.printFlow(flow)
        return x

    def minX(self,listofpairs, alledges):
      x=[]
      for pair in listofpairs:
          flow=MinCostFlow.minCostFlow(pair[0],pair[1],pair[2],alledges,False)
          if(len(flow)==0):
            print "Infeasible, exit."
            return
          x.append(flow)
      return x

    def maxRatio(self,usedbw,budget):
      lambda_0=0
      for k in usedbw:
        ratio=float(usedbw[k])/float(k.capacity)
        print "ratio:"+str(ratio)
        if ratio>lambda_0:
          lambda_0=ratio
      totalcost=sum([usedbw[k]*k.cost for k in usedbw])
      if float(totalcost)/float(budget)>lambda_0:
        lambda_0=float(totalcost)/float(budget)
      print "ratio:"+str(float(totalcost)/float(budget))
      return lambda_0

    def determineP2(self,usedbw,alledges,y,minx,epsilon,lambda_,budget):
      ytax=sum([(e.cost+e.beta)*usedbw.get(e,0) for  e in alledges])
      usedbw_new=self.usedBW(minx)
      cpy=sum([(e.cost+e.beta)*usedbw_new.get(e,0) for e in alledges])
      yb=sum([y[i]*alledges[i].capacity for i in range(len(alledges))])+y[len(alledges)]*budget
      if (ytax-cpy)<=(epsilon*(ytax+lambda_*yb)):
        return True
      else:
        return False

    def usedBW(self,x):
      usedbw={}
      for flow in x:
        for link in flow:
          if(link[0] in usedbw):
            usedbw[link[0]]=usedbw[link[0]]+link[1]
          else:
            usedbw[link[0]]=link[1]
      return usedbw

    def printFlow(self,flow):
        for link in flow:
          print "edge: %s [%s]"%(link[0],link[1])