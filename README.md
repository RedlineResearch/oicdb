oicdb
=====

## Omniscient Interrogative C Debugger

Run:
<<<<<<< HEAD

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
=======
>    $ ./pass.py c_files/tree.c > c_out/tree.c
>    $ cd c_out
>    $ gcc tree.c
>    $ mkfifo debug_fifo
>    $ while [ 1 ]; do cat debug_fifo; done

Then in a separate terminal:
>    $ cd c_out
>    $ ./a.out debug_fifo
>>>>>>> 38d486ddc78859174685eb82a37275f9df916854

And you will see the binary trace print on the screen of the first terminal.

