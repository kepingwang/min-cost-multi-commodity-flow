import networkx as nx

class MinCostFlow:
  @staticmethod
  def minCostFlow(src,dst,bw,edges,all=False):
    #print "Find flow %s->%s: %s"%(src,dst,bw)
    #for e in edges:
    #  print str(e)
    G = nx.DiGraph()
    G.add_node(src, demand = bw)
    G.add_node(dst, demand = -bw)
    vtoe={}
    res=[]
    for e in edges:
      if(e.getAVLBW(all)>0):
      #  print "v: %s v: %s  bw: %s"%(e.v1,e.v2, e.getAVLBW(all))
        G.add_edge(e.v1, e.v2, weight = e.cost+e.beta, capacity = e.getAVLBW(all))
        G.add_edge(e.v2, e.v1, weight = e.cost+e.beta, capacity = e.getAVLBW(all))
        vtoe[(e.v1,e.v2)]=e
        vtoe[(e.v2,e.v1)]=e
    try:
#      print G.edges
      flowDict = nx.min_cost_flow(G)
      for k in flowDict:
        for j in flowDict[k]:
          if flowDict[k][j]>0:
            res.append([vtoe[(k,j)],flowDict[k][j]])
    except nx.exception.NetworkXUnfeasible:
      print "No feasible Flow"
    return res

