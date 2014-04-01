import pycparser
from pycparser.c_ast import *
"""
This contains useful functions for interacting with / changing
a pycparser AST.
"""

def sar(obj, cls, cb):
  """ Performs a recursive DFS on the given object, replacing all
  objects of instance cls with the return value of cb(object_of_type_cls).
  Any objects with __dict__ support will work """
  if isinstance(obj, cls): return cb(obj)
  if isinstance(obj, list): return map(lambda o: sar(o,cls,cb), obj)
  if not hasattr(obj, "__dict__"): return obj
  for k in obj.__dict__.keys():
    obj.__dict__[k] = sar(obj.__dict__[k], cls, cb)
  return obj

search_and_replace = sar

def replace_nodes(ast, cls, cb):
  """ Does a recursive DFS on the given AST, calling cb() on each
  instance of a node / object found which is of type cls. """
  sar(ast, cls, cb)

def sar_string(ast, find, replace):
  return ast_ops.sar(ast, str, lambda s: replace if s == find else s)

