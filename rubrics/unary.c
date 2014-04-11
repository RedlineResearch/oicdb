
int __DEBUG_FIFO = 0; // added
int LVALUE;
typedef int typeofLVALUE;

int main(int argc, char *argv[]) {
  char __DEBUG_ID = (char)0;
  typeofLVALUE *__DEBUG_LVALUE = &(LVALUE);
  write(__DEBUG_FIFO, (const void *)&__DEBUG_ID, sizeof(__DEBUG_ID));
  write(__DEBUG_FIFO, (const void *)(&__DEBUG_LVALUE), sizeof(__DEBUG_LVALUE));
  (*__DEBUG_LVALUE)++;
}

