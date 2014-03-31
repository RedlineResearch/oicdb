#!/usr/bin/env python
import pycparser
import sys
import struct
import pickle

""" A proof-of-concept trace listener for C programs.
This needs to be a lot more efficient (i.e. written in C)
for it to be able to handle an actual C program """

if len(sys.argv) != 3:
  print "Usage: %s symbol_table.pkl debug.fifo"%(sys.argv[0],)
  exit()

sym_table = pickle.load(open(sys.argv[1], 'r'))
fifo = open(sys.argv[2], 'r')

while True:
  data = fifo.read(8)
  if len(data) == 0:
    fifo.close()
    print "Re-opening fifo..."
    fifo = open(sys.argv[2], 'r')
    continue
  ID,val = struct.unpack("@ii",data)
  fn,coord,var = sym_table[ID]
  print "%04d] %s:%d: %s = %d"%(ID,fn,coord.line,var,val)


