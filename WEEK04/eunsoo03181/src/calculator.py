# 파일명: calculator.py

def sum_numbers(*args: int) -> int:
    output = 0
    for i in args:
        output += i
    return output


def multiply(*args: int) -> int:
    output = 1
    for i in args:
        output *= i
    return output


def factorial(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    return factorial(n-1) * n


def fibonacci(n: int) -> int:
    if n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)



def primes_up_to_n(n: int) -> int:
    
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num / 2) + 1):
            if num % i == 0:
                return False
        return True
    
    return [a 
            for a in range(2, n + 1) 
            if is_prime(a)
            ]


def even_numbers(numbers: list[int]) -> list[int]:
    isEven = lambda x: x % 2 == 0
    return list(filter(isEven, numbers))