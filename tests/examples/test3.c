#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int SLEEP = 200000;

void printHello() {
    usleep(SLEEP);
    printf("In printHello()\n");
    printf("Hello, \n");
    Add(5, 6);
    printWorld();
}

void printWorld() {
    usleep(SLEEP);
    printf("In printWorld()\n");
    printf("World!\n");
    Multiply(5, 6);
}

void Add(int a, int b) {
    usleep(SLEEP);
    printf("In Add()\n");
    int sum = a + b;
    printNumber(sum);
}

void Multiply(int a, int b) {
    usleep(SLEEP);
    printf("In Multiply()\n");
    int product = a * b;
    Square(product);
}

void Square(int num) {
    usleep(SLEEP);
    printf("In Square()\n");
    int square = num * num;
    printNumber(square);
}

void printNumber(int num) {
    usleep(SLEEP);
    printf("In printNumber()\n");
    printf("%d\n", num);
}

int main() {
    printHello();
    return 0;
}
