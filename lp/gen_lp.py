#!/usr/bin/env python3

import sys, os
import graph_utils
from functools import reduce
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputfile", help="input .net file")
parser.add_argument("--digraph", help="convert the input graph to digraph",
                    action="store_true")
parser.add_argument("--debug", help="debug mode print out current constraint count",
                    action="store_true")

# variables f_{(req, edge)}
# objective is to minimize the total cost

# subject to:
# bandwidth constraints
# flow conservation constraints
# capacity constraints

temp_objective_file = ".temp_objective.txt"
temp_constraints_file = ".temp_constraints.txt"
temp_bounds_file = ".temp_bounds.txt"


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
  def write_objective(self, filename):
    first_var = True
    with open(filename, 'w') as f:
      f.write("Minimize\n")
      for (req, edge), varname in self.var_dict.items():
        if first_var:
          f.write("{} {}".format(edge.cost, varname))
          first_var = False
        else:
          f.write(" + {} {}".format(edge.cost, varname))
      f.write("\n")
  def write_bounds(self, filename):
    with open(filename, 'w') as f:
      f.write("Bounds\n")
      for _, varname in self.var_dict.items():
        f.write("0 <= {} <= +inf\n".format(varname))
      f.write("\n")
      f.write("End\n")
  def __str__(self):
    res = "\ variable dictionary:\n"
    for req_edge_pair, varname in self.var_dict.items():
      res += "\ {}: {}\n".format(varname, req_edge_pair)
    return res

class MultiCommMinCostFlowLP():
  def __init__(self, graph, outfilename, debug=False):
    self.var = VarReg()
    self.debug = debug
    self.graph = graph
    self.constraint_count = 1
    self.write_constraints(temp_constraints_file)
    self.var.write_objective(temp_objective_file)
    self.var.write_bounds(temp_bounds_file)
    with open(outfilename, 'w') as fout:
      for tempfilename in [temp_objective_file, temp_constraints_file, temp_bounds_file]:
        with open(tempfilename, 'r') as fin:
            for line in fin:
                fout.write(line)
    for tempfilename in [temp_objective_file, temp_constraints_file, temp_bounds_file]:
      os.remove(tempfilename)
    print("LP problem written in {}".format(outfilename))

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

  def write_constraints(self, filename):
    with open(filename, 'w') as f:
      f.write("Subject To\n")
    self._bandwidth_constraints(self.graph, filename)
    self._flow_conservation_constraints(self.graph, filename)
    self._capacity_constraints(self.graph, filename)
  
  def _bandwidth_constraints(self, graph, filename):
    """ # req * # nodes
    """
    with open(filename, 'a') as f:
      f.write("\\ Requirement (Bandwidth) Constraints\n")
      for req in graph.reqs:
        if graph.edges_out(req.src):
          res = "{flow_req_src} >= {req_val}\n".format(
            flow_req_src = self.flows_r(req, graph.edges_out(req.src)),
            req_val = req.val
          )
          f.write(res)
          self._count_constraint()

  def _flow_conservation_constraints(self, graph, filename):
    """ # edge * # req
    """
    with open(filename, 'a') as f:
      f.write("\\ Flow Conservation Constraints\n")
      for node in graph.nodes:
        for req in graph.reqs:
          if node not in (req.src, req.dst):
            res = ""
            if graph.edges_in(node):
              res += self.flows_r(req, graph.edges_in(node))
            if graph.edges_out(node):
              res += " - " + self.flows_r(req, graph.edges_out(node), sep=" - ")
            if res != "":
              res += " = 0\n"
              f.write(res)
            self._count_constraint()

  def _capacity_constraints(self, graph, filename):
    """ # edge * # req
    """
    with open(filename, 'a') as f:
      f.write("\\ Capacity Constraints\n")
      for edge in graph.edges:
        if graph.reqs:
          res = "{flow_edge} <= {edge_cap}\n".format(
            flow_edge = self.flows_e(edge, graph.reqs),
            edge_cap = edge.cap
          )
          f.write(res)
          self._count_constraint()

  @property
  def var_dict(self):
    return self.var


if __name__ == '__main__':
  args = parser.parse_args()
  graph = graph_utils.read_graph(args.inputfile)
  if args.digraph:
    graph = graph_utils.convertToDiGraph(graph)
  lp = MultiCommMinCostFlowLP(graph, args.inputfile+".lp", debug=args.debug)
  if args.debug:
    print(lp.var_dict)

