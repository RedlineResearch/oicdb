import pycparser
from pycparser.c_ast import *
import copy
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
  return sar(ast, str, lambda s: replace if s == find else s)

def sar_ID(ast, find_name, replace, deepcopy=True):
  return sar(ast, ID, lambda i: i if i.name != find_name else copy.deepcopy(replace) if deepcopy else replace)

def find_string(obj, string):
  ret = [None]
  def find_str(s):
    if s.find(string) > -1: ret.append(s)
    return s
  sar(obj, str, find_str)
  return ret[-1]

def fix_typeofs(ast):
  def fix_typeof(td):
    s = td.type.names[0]
    if s.startswith('typeof'):
      td.type = FuncCall(ID("typeof"), ExprList([ID(s[6:])]))
    return td
  return sar(ast, TypeDecl, fix_typeof)

"""
  def fix_typeof(decl):
    s = find_string(decl, "typeof")
    if s:
      def typedecl(td):
        
      sar(decl, TypeDecl, typedecl)
      sar_string(decl, s, "typeof("+s[6:]+")")
    return decl
  return sar(ast, Decl, fix_typeof)
"""

