#!/usr/bin/env python
import pycparser
from pycparser import parse_file
import pickle
import os
import glob

def grab_main(fn, cpp_path='cpp'):
  ast = parse_file(fn, use_cpp=True, cpp_path=cpp_path, \
                   cpp_args=r'-Ifake_libc')
  for c in ast.children():
    #print node.__class__
    node = c[1]
    if isinstance(node,pycparser.c_ast.FuncDef) and node.decl.name == 'main':
      return node.body
  print "No main() found in '%s'"%fn
  return None

for fn in glob.glob("rubrics/*.c"):
  pickle.dump(grab_main(fn), open(fn[:-2]+".pkl", 'w'))

"""
pickle.dump(grab_main("rubrics/setup.c"), open("rubrics/setup.pkl", 'w'))
pickle.dump(grab_main("rubrics/fncn.c"), open("rubrics/fncn.pkl", 'w'))
pickle.dump(grab_main("rubrics/var.c"), open("rubrics/var.pkl", 'w'))
pickle.dump(grab_main("rubrics/return.c"), open("rubrics/return.pkl", 'w'))
pickle.dump(grab_main("rubrics/param.c"), open("rubrics/param.pkl", 'w'))
pickle.dump(grab_main("rubrics/unary.c"), open("rubrics/unary.pkl", 'w'))
"""

