oicdb
=====

## Omniscient Interrogative C Debugger

Run:

```
$ ./pass.py c_files/tree.c > c_out/tree.c
$ cd c_out
$ gcc tree.c
$ mkfifo debug_fifo
$ while [ 1 ]; do cat debug_fifo; done
```

Then in a separate terminal:

```
$ cd c_out
$ ./a.out debug_fifo
```

And you will see the binary trace print on the screen of the first terminal.

### TODO:
1.    ~~Finish "entering" and "exiting" function trace information.~~
2.    Handle "#include" / "typedef" lines more robustly.
3.    Handle Compound statements without using a fake FuncCall.
4.    Save symbol table to file for use by trace listener.
5.    Make a trace listener (read in a pickle file with symbol table / dict
      and convert binary trace to human-readable format).

