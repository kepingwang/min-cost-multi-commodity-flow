class Edge:
    def __init__(self,edgeid,v1,v2,pcapacity,pcost):
        self.active=True
        self.id=edgeid
        self.capacity=pcapacity
        self.cost=pcost
        self.beta=0
        self.usedDualL=0
        self.avlBW=pcapacity
        self.v1=v1
        self.v2=v2

    def pairVertex(self,v):
        if v==self.v1:
            return self.v2
        else:
            return self.v1
    
    def getAVLBW(self,all=False):
      if all:
        return self.capacity
      else:
        return self.avlBW

    def getAVLDualL(self):
        return self.cost+self.beta-self.usedDualL

    def useDualL(self,l):
        print "use dualL:"+str(l)
        print self.v1
        print self.v2
        self.usedDualL+=l
        if self.getAVLDualL()<1e-9:
            return True
        else:
            return False
    def extendBeta(self,b):
        self.beta+=b

    def useBW(self,bw):
        self.avlBW-=bw

    def __str__(self):
      s=str(self.v1)+" "+str(self.v2)+" capacity: "+str(self.capacity)+" cost: "+str(self.cost)+" beta: "+str(self.beta) +" AVLBW: "+str(self.getAVLBW())
      return s
