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
  return ID_count


fncn_rubric = pickle.loads(open("rubrics/fncn.pkl", 'r').read())
def fncn_pass(ast, filename=""):
  """ Insert 'entering' and 'exiting' fncn expressions """
  rubric = fncn_rubric
  
  def var_declare(name):
    decl = copy.deepcopy(rubric.block_items[0])
    decl.init.value = str(ID_count)
    decl.type.declname = name
    return decl
  
  for c in ast.ext:
    # Find all function definitions:
    if isinstance(c, pycparser.c_ast.FuncDef):
      # Append "entering" and "exiting" printfs to block items list:
      rubric_loc = copy.deepcopy(rubric)
      unique_ID = new_sym((filename,c.coord,c.decl.name))
      name = "__DEBUG_"+str(ID_count)
      decl = var_declare(name)
      ast_ops.sar(rubric_loc, str, lambda s: name if s == "__DEBUG_ID" else s)
      fncn_in = rubric_loc.block_items[1]
      fncn_out = rubric_loc.block_items[2]
      c.body.block_items = [decl,fncn_in] + c.body.block_items + [fncn_out]
      ast_ops.sar(c, pycparser.c_ast.Return, lambda r: Compound([fncn_out,r],coord=r.coord))

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
    unique_ID = "__DEBUG_"+str(new_sym((filename,n.coord,n.lvalue.name)))
    ast_ops.sar(ID, str, lambda s: unique_ID if s == "__DEBUG_ID" else s)
    return ID
  # Create AST for writing the variable var to debug FIFO
  def var_var(name):
    var = copy.deepcopy(rubric.block_items[2])
    ast_ops.sar(var, str, lambda s: name if s == "var" else s)
    return var
  
  def dbg(a):
    ID = var_ID(a.lvalue.name, a)
    var = var_var(a.lvalue.name)
    decl = var_declare("__DEBUG_"+str(ID_count))
    a.rvalue = ast_ops.sar(a.rvalue, Assignment, dbg) # let's recurse some more
    cmpd = Compound([decl,a,ID,var,a.lvalue], coord=a.coord)
    return FuncCall(pycparser.c_ast.ID(""), ExprList([cmpd]))
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
  var_pass(ast, filename=sys.argv[1]) # do VAR pass first (don't want to VAR the setup...)
  fncn_pass(ast, filename=sys.argv[1]) # do FNCN pass 2nd (entering main() goes after SETUP expressions)
  setup_pass(ast) # do SETUP pass last
  # TODO: get rid of this hacky line:
  print (subprocess.check_output("cat %s | egrep '^#include'"%(sys.argv[1],), shell=True)).rstrip()
  print "#include <unistd.h>"
  print "#include <fcntl.h>"
  print "int __DEBUG_FIFO;"
  print (to_c(ast))
  pickle.dump(sym_table, open(sym_table_fn, 'w'))

