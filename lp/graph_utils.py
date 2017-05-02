class Req():
  """
  Requirement of a flow between one (src, dst) pair
  """
  def __init__(self, src, dst, val):
    self._src = src
    self._dst = dst
    self._val = val
  @property
  def src(self):
    return self._src
  @property
  def dst(self):
    return self._dst
  @property
  def val(self):
    return self._val
  def __repr__(self):
    return "src: {}, dst: {}, val: {}".format(
      self.src, self.dst, self.val
    )
  def __str__(self):
    return "{} {} {}".format(
      self.src, self.dst, self.val
    )

class Edge():
  """
  One edge from v1 to v2 with capacity and cost.
  """
  def __init__(self, v1, v2, cap, cost):
    self._v1 = v1
    self._v2 = v2
    self._cap = cap
    self._cost = cost
  @property
  def v1(self):
    return self._v1
  @property
  def v2(self):
    return self._v2
  @property
  def cap(self):
    return self._cap
  @property
  def cost(self):
    return self._cost
  def __repr__(self):
    return "v1: {}, v2: {}, cap: {}, cost: {}".format(
      self.v1, self.v2, self.cap, self.cost
    )
  def __str__(self):
    return "{} {} {} {}".format(
      self.v1, self.v2, self.cap, self.cost
    )

class Graph():
  """
  A graph with capacitatied and per-unit-cost edges, and
  (src, dst) pairs flow requirements.
  """
  def __init__(self, num_nodes):
    self._num_nodes = num_nodes
    self._nodes = [v for v in range(num_nodes)]
    self._edges = []
    self._reqs = []
    self._edges_in = [[] for v in range(num_nodes)]
    self._edges_out = [[] for v in range(num_nodes)]
  @property
  def num_nodes(self):
    return self._num_nodes
  @property
  def nodes(self):
    return self._nodes
  @property
  def edges(self):
    return self._edges
  @property
  def reqs(self):
    return self._reqs
  def add_edge(self, edge):
    self._edges.append(edge)
    self._edges_in[edge.v2].append(edge)
    self._edges_out[edge.v1].append(edge)
  def add_req(self, req):
    self._reqs.append(req)
  def edges_out(self, node): # the slowest implementation
    return self._edges_out[node]
  def edges_in(self, node):
    return self._edges_in[node]
  def __str__(self):
    num_node_str = "{}\n".format(self.num_nodes)
    edges_str = ''.join([edge.__str__()+'\n' for edge in self.edges])
    reqs_str = ''.join([req.__str__()+'\n' for req in self.reqs])
    return "{}# egdes: v1 v2 cap cost\n{}requirements: src dst value\n{}\n".format(
      num_node_str, edges_str, reqs_str
    )
  
def nums(string):
  return [int(s) for s in string.split()]

def read_graph(filename):
  graph = None
  reading_area = 'num_nodes'
  with open(filename, 'r') as f:
    for line in f:
      line = line.strip()
      if len(line) == 0 or line[0] == '#':
        continue
      if reading_area == 'num_nodes':
        graph = Graph(nums(line)[0])
        reading_area = 'edges'
      elif reading_area == 'edges':
        if not line[0].isalpha():
          edge = Edge(*tuple(nums(line)))
          graph.add_edge(edge)
        else:
          reading_area = 'requirements'
      elif reading_area == 'requirements':
        req = Req(*tuple(nums(line)))
        graph.add_req(req)
  return graph


def convertToDiGraph(graph):
  digraph = Graph(graph.num_nodes * 2)
  for e in graph.edges:
    edge1 = Edge(e.v1, e.v2, e.cap, e.cost)
    edge2 = Edge(e.v2, e.v1, e.cap, e.cost)
    digraph.add_edge(edge1)
    digraph.add_edge(edge2)
  for req in graph.reqs:
    digraph.add_req(req)
  return digraph
    
    
