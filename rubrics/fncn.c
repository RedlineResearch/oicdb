
int __DEBUG_FIFO = 0; // added

int main(int argc, char *argv[]) {
  write(__DEBUG_FIFO, "Entering fncn %s.\n", 20); //fsync(__DEBUG_FIFO);
  write(__DEBUG_FIFO, "Exiting fncn %s.\n", 19); //fsync(__DEBUG_FIFO); // added
}

