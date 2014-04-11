
int __DEBUG_FIFO = 0; // added
int var, LVALUE, RVALUE;
typedef int typeofLVALUE;
typedef int typeofRVALUE;

int main(int argc, char *argv[]) {
  char __DEBUG_ID = (char)0;
  typeofLVALUE *__DEBUG_LVALUE = &(LVALUE);
  typeofRVALUE  __DEBUG_RVALUE = RVALUE;
  write(__DEBUG_FIFO, (const void *)&__DEBUG_ID, sizeof(__DEBUG_ID));
  __DEBUG_ID = sizeof(__DEBUG_LVALUE);
  write(__DEBUG_FIFO, (const void *)&__DEBUG_ID, sizeof(__DEBUG_ID));
  write(__DEBUG_FIFO, (const void *)(&__DEBUG_LVALUE), sizeof(__DEBUG_LVALUE));
  //printf("%d\n", (int)sizeof(__DEBUG_RVALUE));
  __DEBUG_ID = sizeof(__DEBUG_RVALUE);
  write(__DEBUG_FIFO, (const void *)&__DEBUG_ID, sizeof(__DEBUG_ID));
  write(__DEBUG_FIFO, (const void *)(&__DEBUG_RVALUE), sizeof(__DEBUG_RVALUE));
}

