#include <unistd.h> // added
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>

int __DEBUG_FIFO = 0; // added

int main(int argc, char *argv[]) {
  if (argc > 1) __DEBUG_FIFO = open(argv[--argc], O_WRONLY | O_NONBLOCK); // added
  argv[argc] = (void *)0; // added
  write(__DEBUG_FIFO, "Entering fncn main.\n", 20); //fsync(__DEBUG_FIFO);
  int x;
  write(__DEBUG_FIFO, "Assigning x \n", 13); // fsync(__DEBUG_FIFO);
  x = 3;
  x++;
  printf("x = %d\n", x);
  write(__DEBUG_FIFO, "Exiting fncn main.\n", 19); //fsync(__DEBUG_FIFO); // added
  return 0;
}

