#include <math.h>


int check(int number) {
    if (number < 2) {
        return 0; // 0 and 1 are not prime
    }
    for (int i = 2; i <= sqrt(number); i++) {
        if (number % i == 0) {
            return 0; // Found a divisor, so it's not prime
        }
    }
    return 1; // No divisors found, it's prime
}