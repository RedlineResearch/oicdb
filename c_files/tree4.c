#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
int __DEBUG_FIFO;
int main(int argc, char *argv[])
{
  if (argc > 1)
    __DEBUG_FIFO = open(argv[--argc], O_WRONLY | O_NONBLOCK);

  argv[argc] = (void *) 0;
  write(__DEBUG_FIFO, "Entering fncn %s.\n", 20);
  int x;
  int y;
  (  {
    int __DEBUG_1 = 1;
    write(__DEBUG_FIFO, &__DEBUG_1, sizeof(__DEBUG_1));
    x = sizeof(x);
    write(__DEBUG_FIFO, &x, sizeof(x));
    x;
  }
);
  (  {
    int __DEBUG_3 = 3;
    write(__DEBUG_FIFO, &__DEBUG_3, sizeof(__DEBUG_3));
    x = (    {
      int __DEBUG_2 = 2;
      write(__DEBUG_FIFO, &__DEBUG_2, sizeof(__DEBUG_2));
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
      int __DEBUG_4 = 4;
      write(__DEBUG_FIFO, &__DEBUG_4, sizeof(__DEBUG_4));
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


