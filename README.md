oicdb
=====

## Omniscient Interrogative C Debugger

Run:

```
$  ./runpass [?.c]
```

which runs pass.py on c_files/?.c saving the output to c_out/?.c,
compiles c_out/?.c, stores the symbol table and corresponding
AST entries to c_out/?.c.sym and recreates the debugging fifo
queue at c_out/debug_fifo.

You can then in separate terminals run:

```
$ cd c_out
$ ../trace.py ?.c.sym.pkl debug_fifo
```

and

```
$ cd c_out
$ ./a.out debug_fifo
```

which produces a human-readable trace of the assignments in the program.

### TODO:
1.    ~~Finish "entering" and "exiting" function trace information.~~
2.    Handle "#include" / "typedef" lines more robustly.
3.    Handle Compound statements without using a fake FuncCall.
4.    ~~Save symbol table to file for use by trace listener.~~
5.    ~~Make a trace listener (read in a pickle file with symbol table / dict
      and convert binary trace to human-readable format).~~
6.    ~~Make a trace listener which handles data types other than int.~~
7.    ~~Figure out why trace of function calls is not working.~~
8.    Label function entrances / exits as such so that trace listener can
      tell the programmer the difference.
9.    Trace listener parse different data types.
10.   Store memory updates in dictionary.

