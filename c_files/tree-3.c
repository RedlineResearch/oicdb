#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int __DEBUG_FIFO;
int __DEBUG_1 = 1;
int __DEBUG_2 = 2;
int __DEBUG_3 = 3;
int __DEBUG_4 = 4;

int main(int argc, char *argv[])
{
  if (argc > 1)
    __DEBUG_FIFO = open(argv[--argc], O_WRONLY | O_NONBLOCK);

  argv[argc] = (void *) 0;
  write(__DEBUG_FIFO, "Entering fncn %s.\n", 20);
  int x;
  int y;
  (  {
    write(__DEBUG_FIFO, &__DEBUG_1, sizeof(1));
    x = sizeof(x);
    write(__DEBUG_FIFO, &x, sizeof(x));
    x;
  }
);
  (  {
    write(__DEBUG_FIFO, &__DEBUG_3, sizeof(3));
    x = (    {
      write(__DEBUG_FIFO, &__DEBUG_2, sizeof(2));
      y = 3;
      write(__DEBUG_FIFO, &y, sizeof(y));
      y;
    }
);
    write(__DEBUG_FIFO, &x, sizeof(x));
    x;
  }
);
  x++;
  printf("x = %d\n", x);
  {
    (    {
      write(__DEBUG_FIFO, &__DEBUG_4, sizeof(4));
      x += 3;
      write(__DEBUG_FIFO, &x, sizeof(x));
      x;
    }
);
    printf("x + 3 = %d\n", x);
  }
  return 0;
  write(__DEBUG_FIFO, "Exiting fncn %s.\n", 19);
}


