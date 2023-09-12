#include <stdio.h>
#include <stdlib.h>

#define MAX_N 121

unsigned long long int fastFib(int n, unsigned long long int memo[]) {
    if (n == 0 || n == 1) {
        return 1;
    }

    if (memo[n] != -1) {
        return memo[n];
    }

    memo[n] = fastFib(n - 1, memo) + fastFib(n - 2, memo);
    return memo[n];
}

int main() {
    unsigned long long int memo[MAX_N];

    for (int i = 0; i < MAX_N; i++) {
        memo[i] = -1;
    }

    for (int i = 0; i < 121; i++) {
        unsigned long long int result = fastFib(i, memo);
        printf("fib(%d) = %llu\n", i, result);
    }

    return 0;
}
