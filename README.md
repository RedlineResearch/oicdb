oicdb
=====

## Omniscient Interrogative C Debugger

Run:

```
$ ./runpass
```

which runs pass.py on c_files/tree.c saving the output to c_out/tree.c,
compiles c_out/tree.c, and creates a new debugging fifo queue named
c_out/debug_fifo.

You can then in separate terminals run:

```
$ cd c_out
$ ../trace.py tree.c.sym.pkl debug_fifo
```

and

```
$ cd c_out
$ ./tree debug_fifo
```

which produces a human-readable trace of the assignments in the program.


And you will see the binary trace print on the screen of the first terminal.

### TODO:
1.    ~~Finish "entering" and "exiting" function trace information.~~
2.    Handle "#include" / "typedef" lines more robustly.
3.    Handle Compound statements without using a fake FuncCall.
4.    Save symbol table to file for use by trace listener.
5.    ~~Make a trace listener (read in a pickle file with symbol table / dict
      and convert binary trace to human-readable format).~~
6.    Make a trace listener which handles data types other than int.
7.    Figure out why trace of function calls is not working.

