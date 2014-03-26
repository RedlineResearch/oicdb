#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
  int x;
  int y;
  x = sizeof(x);
  x = (y = 3);
  x++;
  printf("x = %d\n", x);
  {
    x += 3;
    printf("x + 3 = %d\n", x);
  }
  return 0;
}

