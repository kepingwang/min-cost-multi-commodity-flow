#!/usr/bin/python
#./network_gen.py #V #pairs
import random
import sys
nvertex=int(sys.argv[1])
npairs=int(sys.argv[2])
edges={}
pairs={}
rrange=[10,30]
crange=[2,10]
nhop=10

def printGraph(nvertex,pairs,edges,name):
  f=open("graph/"+name+".net","w")
  f.write(str(nvertex)+"\n")
  f.write("#edges v1 v2 capacity cost\n")
  for e in edges:
    cost=random.randint(crange[0],crange[1])
    f.write(str(e[0])+" "+str(e[1])+" "+str(edges[e])+" "+str(cost)+"\n")
  f.write("requirements:\n")
  for r in pairs:
    f.write(str(r[0])+" "+str(r[1])+" "+str(pairs[r])+"\n")
  f.close()

for i in range(npairs):
  v1=random.randint(0,nvertex-1)
  v2=random.randint(0,nvertex-1)
  if v1!=v2 and (v1,v2) not in pairs and (v2,v1) not in pairs:
    r=random.randint(rrange[0],rrange[1])
    pairs[(v1,v2)]=r
    lastv=v1
    for j in range(nhop):
      medh=random.randint(0,nvertex-1)
      while medh==lastv or medh==v2:
        medh=random.randint(0,nvertex-1)
      vv1=min(lastv,medh)
      vv2=max(lastv,medh)
      if (vv1,vv2) in edges:
        val=edges[(vv1,vv2)]
        edges[(vv1,vv2)]=val+r
      else:
        edges[(vv1,vv2)]=r
      lastv=medh
    vv1=min(lastv,v2)
    vv2= max(lastv, v2)
    if (vv1,vv2) in edges:
      val=edges[(vv1,vv2)]
      edges[(vv1,vv2)]=val+r
    else:
      edges[(vv1,vv2)]=r

printGraph(nvertex,pairs,edges,sys.argv[3])

