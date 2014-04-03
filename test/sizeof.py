execfile("../ast_ops.py")
from pycparser import parse_file
import sys
import glob

sep = "-"*10

get_ast = lambda fn: parse_file(fn, use_cpp=True, cpp_path='cpp', cpp_args=r'-I../fake_libc')

for fn in glob.glob("../c_files/*.c"):
  ast1 = get_ast(fn)
  sar(ast1, Decl, lambda d: sys.stdout.write("sizeof(%s) = %d\n"%(d.name,sizeof(d))))
  print sep


