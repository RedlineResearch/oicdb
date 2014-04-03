import pycparser
from pycparser.c_ast import *
import copy
import ctypes
import StringIO
import pexpect
import os

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

csize = ctypes.sizeof
type_sizes = {
  "bool":   csize(ctypes.c_bool),
  "byte":   csize(ctypes.c_byte),
  "char":   csize(ctypes.c_char),
  "double": csize(ctypes.c_double),
  "float":  csize(ctypes.c_float),
  "int":    csize(ctypes.c_int),
  "long":   csize(ctypes.c_long),
  "long double": csize(ctypes.c_longdouble),
  "short":  csize(ctypes.c_short),
  "unsigned byte": csize(ctypes.c_ubyte),
  "unsigned int": csize(ctypes.c_uint),
  "unsigned long": csize(ctypes.c_ulong),
  "unsigned short": csize(ctypes.c_short),
  "char": csize(ctypes.c_wchar),
}

def gcc_get_size(name):
  """ Magically computes the size of a C data type """
  proc = pexpect.spawn("gcc -o .gcc_get_size.o -xc -")
  proc.send("#include <stdio.h>\n")
  proc.send("void main(int argc, char *argv[]) {\n")
  proc.send("  int x = (int)sizeof(%s);\n"%name)
  proc.send("  printf(\"%d\", x);\n")
  proc.send("}\n")
  proc.sendcontrol('d')
  #print proc.readlines()
  size = int(pexpect.run("./.gcc_get_size.o"))
  os.remove("./.gcc_get_size.o")
  return size

def get_size(names):
  if len(names) == 0: raise Exception("Error gettings size of NIL type")
  name = " ".join(names)
  if name not in type_sizes.keys():
    type_sizes[name] = gdb_get_size(name)
  return type_sizes[name]

def sizeof(decl):
  """ Computes the number of bytes the given pycparser AST Decl takes up as a C data type """
  typ = type(decl)
  if typ in [ArrayDecl,PtrDecl]: return csize(ctypes.c_void_p)
  # constraint violation of sizeof(), so returning 1 to conform with GCC sizeof()
  elif typ == FuncDecl: return 1
  elif typ == TypeDecl: return sizeof(decl.type)
  elif typ == IdentifierType: return get_size(decl.names)
  elif typ == Decl: return sizeof(decl.type)
  else:
    buf = StringIO.StringIO()
    decl.show(buf=buf)
    raise Exception("Unhandled Decl type in typeof():\n"+buf.getvalue())


