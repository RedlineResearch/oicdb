/* merge.c -- Given two sorted sequences of integers, it creates
 *            a sorted sequence consisting of all their numbers.
 */

#include <stdio.h>

#define NMAX 100

void printIntArray(int a[], int n);
void merge(int c[], int *nc, int a[], int na, int b[], int nb);

int main(int argc, char **argv) {
  int x[NMAX] = {1,3,5,6,7,8,10,11,15,20,21,21,22,24,26,28,29,32,34,35}; /* The first sorted sequence */
  int y[NMAX] = {2,3,4,6,6,9,10,12,16,21,23,23,26,27,29,33,35,39,40,41}; /* The second sorted sequence */
  int z[NMAX+NMAX]; /* The merge sequence */
  int nz;

  merge(z,&nz,x,20,y,20);
  printIntArray(z,nz);
}

void printIntArray(int a[], int n)
     /* n is the number of elements in the array a.
      * These values are printed out, five per line. */
{
  int i;

  for (i=0; i<n; i++){
    printf("\t%d ", a[i]);
    if (i%5==4)
      printf("\n");
  }
  printf("\n");
}

void merge(int c[], int *nc, int a[], int na, int b[], int nb){
  /* Given sorted sequences a and b, respectively with na and nb
   * elements, it stores their merge sequence in c and returns 
   * the total number of elements in nc
   */
  int cursora = 0, cursorb = 0, cursorc = 0;

  while((cursora<na)&&(cursorb<nb))
    if (a[cursora]<=b[cursorb]) {
      c[cursorc]=a[cursora];
      cursorc++;
      cursora++;
    }    
    else {
      c[cursorc]=b[cursorb];
      cursorc++;
      cursorb++;
    }

  while(cursora<na) {
    c[cursorc]=a[cursora];
    cursorc++;
    cursora++;
  }

  while(cursorb<nb) {
    c[cursorc]=b[cursorb];
    cursorc++;
    cursorb++;
  }

  *nc = cursorc;
}
