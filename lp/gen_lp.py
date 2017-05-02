#!/usr/bin/env python3

import sys
import graph_utils
from functools import reduce
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile", help="input .net file")
parser.add_argument("-d", "--digraph", help="convert the input graph to digraph",
                    action="store_true")
parser.add_argument("--debug", help="debug mode print out current constraint count",
                    action="store_true")

# variables f_{(req, edge)}
# objective is to minimize the total cost

# subject to:
# bandwidth constraints
# flow conservation constraints
# capacity constraints



class VarReg():
  """
  String registration for flows with req commodity and edge.
  """
  def __init__(self):
    self.count = 1
    self.var_dict = {}
  def get(self, req, edge):
    if (req, edge) in self.var_dict:
      return self.var_dict[(req, edge)]
    else:
      self.var_dict[(req, edge)] = "x" + str(self.count)
      self.count += 1
      return self.var_dict[(req, edge)]
  def min_cost_expr(self):
    return reduce(
      lambda var1, var2: var1 + " + " + var2,
      ["{} {}".format(edge.cost, varname)
       for (req, edge), varname in self.var_dict.items()]
    )
  def bounds(self):
    return reduce(
      lambda x, y: x + y,
      ["0 <= {} <= +inf\n".format(varname)
       for _, varname in self.var_dict.items()]
    )
  def __str__(self):
    res = "\ variable dictionary:\n"
    for req_edge_pair, varname in self.var_dict.items():
      res += "\ {}: {}\n".format(varname, req_edge_pair)
    return res

class MultiCommMinCostFlowLP():
  def __init__(self, graph, debug=False):
    self.var = VarReg()
    self.debug = debug
    self.constraint_count = 1
    self._constraints = "Subject To\n"
    self._constraints += "\ Bandwidth Constraints\n"
    self._constraints += self._bandwidth_constraints(graph)
    self._constraints += "\ Flow Conservation Constraints\n"
    self._constraints += self._flow_conservation_constraints(graph)
    self._constraints += "\ Capacity Constraints\n"
    self._constraints += self._capacity_constraints(graph)
    self._constraints += "\n"
    self._objective = "Minimize\n"
    self._objective += self.var.min_cost_expr()
    self._objective += "\n\n"
    self._bounds = "Bounds\n"
    self._bounds += self.var.bounds()
    self._bounds += "\n"
    self._lp_expression = self._objective \
                          + self._constraints + self._bounds + "End\n\n"

  def _count_constraint(self):
    if self.debug:
      print("constraint count: {}".format(self.constraint_count))
    self.constraint_count += 1
    
  def flows_r(self, req, edges, sep=" + "):
    return reduce(
      lambda x, y: x + sep + y,
      [self.var.get(req, edge) for edge in edges]
    )
  def flows_e(self, edge, reqs, sep=" + "):
    return reduce(
      lambda x, y: x + sep + y,
      [self.var.get(req, edge) for req in reqs]
    )

  
  
  def _bandwidth_constraints(self, graph):
    """ # req * # nodes
    """
    res = ""
    for req in graph.reqs:
      if graph.edges_out(req.src):
        res += "{flow_req_src} >= {req_val}\n".format(
          flow_req_src = self.flows_r(req, graph.edges_out(req.src)),
          req_val = req.val
        )
        self._count_constraint()
    return res

  def _flow_conservation_constraints(self, graph):
    """ # edge * # req
    """
    res = ""
    for node in graph.nodes:
      for req in graph.reqs:
        if node not in (req.src, req.dst):
          if graph.edges_in(node):
            res += self.flows_r(req, graph.edges_in(node))
          if graph.edges_out(node):
            res += " - " + self.flows_r(req, graph.edges_out(node), sep=" - ")
          if res != "":
            res += " = 0\n"
            self._count_constraint()
    return res

  def _capacity_constraints(self, graph):
    """ # edge * # req
    """
    res = ""
    for edge in graph.edges:
      if graph.reqs:
        res += "{flow_edge} <= {edge_cap}\n".format(
          flow_edge = self.flows_e(edge, graph.reqs),
          edge_cap = edge.cap
        )
        self._count_constraint()
    return res

  @property
  def var_dict(self):
    return self.var
  @property
  def lp_expression(self):
    return self._lp_expression

if __name__ == '__main__':
  args = parser.parse_args()
  graph = graph_utils.read_graph(args.inputfile)
  if args.digraph:
    graph = graph_utils.convertToDiGraph(graph)
  lp = MultiCommMinCostFlowLP(graph, args.debug)
  if args.debug:
    print(lp.var_dict)
  print(lp.lp_expression)
