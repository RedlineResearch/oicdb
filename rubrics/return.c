
int __DEBUG_FIFO = 0; // added
int ret;

int main(int argc, char *argv[]) {
  char __DEBUG_ID = (char)0;
  int __DEBUG_RETURN = ret;
  write(__DEBUG_FIFO, (const void *) (&__DEBUG_ID), sizeof(__DEBUG_ID)); //fsync(__DEBUG_FIFO);
  __DEBUG_ID = (int)sizeof(__DEBUG_RETURN);
  write(__DEBUG_FIFO, (const void *) (&__DEBUG_ID), sizeof(__DEBUG_ID));
  write(__DEBUG_FIFO, (const void *) (&__DEBUG_RETURN), sizeof(__DEBUG_RETURN));
  return __DEBUG_RETURN;
}

