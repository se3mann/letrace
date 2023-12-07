#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void functionA() {
    printf("functionA\n");
    sleepFunction();
    functionB();
}

void functionB() {
    printf("functionB\n");
    sleepFunction();
    functionC();
    functionD();
}

void functionC() {
    printf("functionC\n");
    sleepFunction();
    functionE();
}

void functionD() {
    printf("functionD\n");
    sleepFunction();
    functionF();
}

void functionE() {
    printf("functionE\n");
    sleepFunction();
    functionF();
    functionD();
}

void functionF() {
    printf("functionF\n");
    sleepFunction();
}

void sleepFunction() {
    usleep(200000); // Sleep for 0.2 seconds
}

int main() {
    functionA();
    return 0;
}