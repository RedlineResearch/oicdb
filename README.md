oicdb
=====

## Omniscient Interrogative C Debugger

Run:
> $ ./pass.py c_files/tree.c > c_out/tree.c
> $ cd c_out
> $ gcc tree.c
> $ mkfifo debug_fifo
> $ while [ 1 ]; do cat debug_fifo; done

Then in a separate terminal:
> $ cd c_out
> $ ./a.out debug_fifo

And you will see the binary trace print on the screen of the first terminal.

