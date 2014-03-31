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
  sym_table[unique_key] = ID_count
  return ID_count


fncn_rubric = pickle.loads(open("rubrics/fncn.pkl", 'r').read())
def fncn_pass(ast, filename=""):
  """ Insert 'entering' and 'exiting' fncn expressions """
  rubric = fncn_rubric
  fncn_in = rubric.block_items[1]
  fncn_out = rubric.block_items[2]
  
  def var_declare(name):
    decl = copy.deepcopy(rubric.block_items[0])
    decl.init.value = str(ID_count)
    decl.type.declname = name
    return decl
  
  # TODO: Find all return statements and convert them into Compounds
  # containing "write('Exiting fncn')" + the return statement. Leave the
  # below code as is in case there isn't a return statement at the end of a
  # void function.
  
  for c in ast.ext:
    # Find all function definitions:
    if isinstance(c, pycparser.c_ast.FuncDef):
      # Append "entering" and "exiting" printfs to block items list:
      unique_ID = new_sym((filename,c.coord,c.decl.name))
      name = "__DEBUG_"+str(ID_count)
      decl = var_declare(name)
      ast_ops.sar(rubric, str, lambda s: name if s == "__DEBUG_ID" else s)
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
    ID.args.exprs[2].expr.name = str(unique_ID)
    #print ID.args.exprs[1].__dict__
    ID.args.exprs[1].expr.name = str(unique_ID)
    return ID
  # Create AST for writing the variable var to debug FIFO
  def var_var(name):
    var = copy.deepcopy(rubric.block_items[2])
    var.args.exprs[2].expr.name = name
    var.args.exprs[1].expr.name = name
    return var
  
  def dbn(n):
    # If we have a list - recursive map onto the list:
    if isinstance(n, list):
      return map(dbn, n) # Compound block_items
    #if hasattr(n, "__dict__"): # debugging...
    #  print n.__dict__
    # If we don't have a Node (likely str, int, etc...) then leave it be:
    if not isinstance(n, Node): return n
    # Recursively map onto all the __dict__ values in the Node object:
    for key in n.__dict__.keys(): #n.children():
      c = n.__dict__[key]
      ret = dbn(c)
      if not (ret == n.__dict__[key]):
        #print "Replacing "+str(n.__dict__[key])+" with "+str(ret)
        n.__dict__[key] = ret
    # If we have an Assignment node, replace it accordingly
    if isinstance(n, Assignment): # Convert Assignment into Compound (write + assig)
      ID = var_ID(n.lvalue.name,n)
      var = var_var(n.lvalue.name)
      decl = var_declare("__DEBUG_"+str(ID_count))
      #print ID.__dict__
      # TODO: Figure out how to make this Compound parenthesized without using a FuncCall...
      return FuncCall(pycparser.c_ast.ID(""), \
                      ExprList([Compound([decl,ID,n,var,n.lvalue],coord=n.coord)]))
    # Not an Assignment, so just leave it be:
    return n

  # TODO: Change e.g. "3" to "__DEBUG_3" and add "int __DEBUG_3" declarations
  # in local scope? (global scope? local is probably easier...) Also, fix / add
  # "#includes" at top of file / in global scope
  
  #dbn(ast.ext)

  def dbg(a):
    ID = var_ID(a.lvalue.name, a)
    var = var_var(a.lvalue.name)
    decl = var_declare("__DEBUG_"+str(ID_count))
    a.rvalue = ast_ops.sar(a.rvalue, Assignment, dbg) # let's recurse some more
    cmpd = Compound([decl,ID,a,var,a.lvalue], coord=a.coord)
    return FuncCall(pycparser.c_ast.ID(""), ExprList([cmpd]))
  ast_ops.sar(ast, Assignment, dbg)



def to_c(ast):
  gen = c_generator.CGenerator()
  return gen.visit(ast)

if __name__ == '__main__':

  if len(sys.argv) != 2:
    print ("Usage: %s [file.c]"%sys.argv[0])
    exit()

  ast = get_ast(sys.argv[1])
  sym_table[sys.argv[1]] = dict()
  var_pass(ast, filename=sys.argv[1]) # do VAR pass first (don't want to VAR the setup...)
  fncn_pass(ast, filename=sys.argv[1]) # do FNCN pass 2nd (entering main() goes after SETUP expressions)
  setup_pass(ast) # do SETUP pass last
  # TODO: get rid of this hacky line:
  print (subprocess.check_output("cat %s | egrep '^#include'"%(sys.argv[1],), shell=True)).rstrip()
  print "#include <fcntl.h>"
  print "int __DEBUG_FIFO;"
  print (to_c(ast))


