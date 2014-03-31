
int __DEBUG_FIFO = 0; // added

int main(int argc, char *argv[]) {
  int __DEBUG_ID = 0;
  write(__DEBUG_FIFO, __DEBUG_ID, sizeof(__DEBUG_ID)); //fsync(__DEBUG_FIFO);
  write(__DEBUG_FIFO, __DEBUG_ID, sizeof(__DEBUG_ID)); //fsync(__DEBUG_FIFO); // added
}

