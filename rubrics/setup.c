//#include <unistd.h> // added
//#include <sys/types.h>
//#include <sys/stat.h>
#include <fcntl.h>
//#include <stdio.h>
//#include <stdlib.h>

int __DEBUG_FIFO = 0; // added

int main(int argc, char *argv[]) {
  if (argc > 1) __DEBUG_FIFO = open(argv[--argc], O_WRONLY | O_NONBLOCK); // added
  argv[argc] = (void *)0; // added
}

