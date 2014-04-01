#!/usr/bin/env python
import pycparser
from pycparser import parse_file, c_generator
from pycparser.c_ast import *
import ast_ops
import sys
import pickle
import copy
import subprocess

sym_table = dict()
ID_count = 0

def get_ast(fn, cpp_path='cpp'):
  return parse_file(fn, use_cpp=True, cpp_path=cpp_path, \
                    cpp_args=r'-Ifake_libc')

setup_rubric = pickle.loads(open("rubrics/setup.pkl", 'r').read())
def setup_pass(ast):
  """ Insert setup expressions into main() as necessary """
  rubric = setup_rubric
  #print ast.ext
  result = []
  for c in ast.ext:
    # Find main():
    if isinstance(c, pycparser.c_ast.Typedef):
      continue
    elif isinstance(c, pycparser.c_ast.FuncDef) and c.decl.name == 'main':
      # Append setup expressions to beginning of main() block items list:
      c.body.block_items = rubric.block_items + c.body.block_items
    result.append(c)
  ast.ext = result
  #print ast.ext
  
# Updates the symbol table to include the new unique key. Return the new
# ID_count so the caller knows the ID for the new symbol / assignment.
def new_sym(unique_key):
  global ID_count, sym_table
  ID_count = ID_count + 1
  sym_table[ID_count] = unique_key
  return "__DEBUG_"+str(ID_count)

def var_declare(name, rubric, num):
  decl = copy.deepcopy(rubric.block_items[num])
  decl.init.value = str(ID_count)
  decl.type.declname = name
  return decl

fncn_rubric = pickle.loads(open("rubrics/fncn.pkl", 'r').read())
def fncn_pass(ast, filename=""):
  """ Insert 'entering' and 'exiting' fncn expressions """
  rubric = fncn_rubric
  
  # Find and debug entrance and void exit of all function definitions:
  def dbg(c):
    rubric_loc = copy.deepcopy(rubric)
    name = new_sym((filename,c.coord,c.decl.name,type(c)))
    decl = var_declare(name, rubric_loc, 0)
    ast_ops.sar_string(rubric_loc, "__DEBUG_ID", name)
    f_in = rubric_loc.block_items[1]
    f_out = rubric_loc.block_items[2]
    c.body.block_items = [decl,f_in] + c.body.block_items + [f_out]
    return c
  ast_ops.sar(ast, pycparser.c_ast.FuncDef, dbg)

return_rubric = pickle.loads(open("rubrics/return.pkl", 'r').read())
def return_pass(ast, filename=""):
  """ Insert 'exiting' fncn expressions at return statements """
  rubric = return_rubric
  
  # Find and debug all return statements:
  def dbg(ret):
    rubric_loc = copy.deepcopy(rubric)
    name = new_sym((filename,ret.coord,"return",type(ret)))
    decl = var_declare(name, rubric_loc, 0)
    ast_ops.sar_string(rubric_loc, "__DEBUG_ID", name)
    fncn_out = rubric_loc.block_items[2]
    decl2 = var_declare("__DEBUG_RETURN", rubric, 1)
    decl2.init = ret.expr
    ret.expr = pycparser.c_ast.ID("__DEBUG_RETURN")
    fncn_ret = rubric_loc.block_items[5]
    return Compound([decl,decl2,fncn_out,rubric_loc.block_items[3],\
                     rubric_loc.block_items[4],fncn_ret,ret],coord=ret.coord)
  ast_ops.sar(ast, pycparser.c_ast.Return, dbg)


var_rubric = pickle.loads(open("rubrics/var.pkl", 'r').read())
def var_pass(ast, filename=""):
  """ Insert assignment to variable logging expressions """
  rubric = var_rubric
  
  # Create AST for variable declaration:
  def var_declare(name):
    decl = copy.deepcopy(rubric.block_items[0])
    decl.init.value = str(ID_count)
    decl.type.declname = name
    return decl
  # Create AST for writing the variable ID to debug FIFO
  def var_ID(name,n):
    ID = copy.deepcopy(rubric.block_items[1])
    unique_ID = new_sym((filename,n.coord,n.lvalue.name,type(n)))
    ast_ops.sar(ID, str, lambda s: unique_ID if s == "__DEBUG_ID" else s)
    return ID
  # Create AST for writing the variable var to debug FIFO
  def var_var(name):
    var = copy.deepcopy(rubric.block_items[2])
    ast_ops.sar(var, str, lambda s: name if s == "var" else s)
    return var
  
  def dbg(a):
    if isinstance(a.lvalue, pycparser.c_ast.ID):
      ID = var_ID(a.lvalue.name, a)
      var = var_var(a.lvalue.name)
      decl = var_declare("__DEBUG_"+str(ID_count))
      a.rvalue = ast_ops.sar(a.rvalue, Assignment, dbg) # let's recurse some more
      cmpd = Compound([decl,a,ID,var,a.lvalue], coord=a.coord)
      return FuncCall(pycparser.c_ast.ID(""), ExprList([cmpd]))
    return a
  ast_ops.sar(ast, Assignment, dbg)

def to_c(ast):
  gen = c_generator.CGenerator()
  return gen.visit(ast)

if __name__ == '__main__':

  if len(sys.argv) < 2:
    print ("Usage: %s file.c [sym_table.pkl]"%sys.argv[0])
    exit()

  fn = sys.argv[1]
  sym_table_fn = fn + ".sym.pkl"
  if len(sys.argv) > 2: sym_table_fn = sys.argv[2] + ".sym.pkl"

  ast = get_ast(fn)
  var_pass(ast, filename=fn) # do VAR pass first (don't want to VAR the setup...)
  fncn_pass(ast, filename=fn) # do FNCN pass 2nd (entering main() goes after SETUP expressions)
  return_pass(ast, filename=fn) # return pass 3rd?
  setup_pass(ast) # do SETUP pass last
  # TODO: get rid of this hacky line:
  print (subprocess.check_output("cat %s | egrep '^#include'"%(sys.argv[1],), shell=True)).rstrip()
  print "#include <unistd.h>"
  print "#include <fcntl.h>"
  print "int __DEBUG_FIFO;"
  print (to_c(ast))
  pickle.dump(sym_table, open(sym_table_fn, 'w'))

