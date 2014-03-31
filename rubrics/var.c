
int __DEBUG_FIFO = 0; // added
int var;

int main(int argc, char *argv[]) {
  int __DEBUG_ID = 0;
  write(__DEBUG_FIFO, (const void *)(&(__DEBUG_ID)), sizeof(__DEBUG_ID));
  write(__DEBUG_FIFO, (const void *)(&(var)), sizeof(var));
}

