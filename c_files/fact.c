#include <stdio.h>

int factorial(int i) {
    if (i <= 1) {
        return 1;
    } else {
        return i * factorial(i - 1);
    }
}

int main(int argc, char **argv) {
    int x = 0;
    const char *string = "The factorial of %d is: %d\n";
    for (int i = 1; i <= 5; i++) {
        x = factorial(i);
        printf(string, i, x);
    }
    x = 10;
    return 0;
}
