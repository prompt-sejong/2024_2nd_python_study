def sum_numbers(*args: int) -> int:
    # 복수 개의 정수 입력을 받아 모두 더한 값을 출력하는 함수
    # for 문을 사용하세요
    output = 0
    for i in args:
        output += i
        return output
    

def multiply(*args: int) -> int:
    # 복수 개의 정수 입력을 받아 모두 곱한 값을 출력하는 함수
    # for 문을 사용하세요

    output = 1
    for i in args:
        output *= i
        return output
    


def factorial(n: int) -> int:
    # n이 0 이상일 때, n! 을 반환하는 함수
    # while 문을 사용하세요
    output = 1
    while n >= 0 :
            output *= n
            n -= 1
    return result



def fibonacci(n: int) -> int:
    # n 번째 피보나치 수를 반환하는 함수
    # 조건문과 재귀함수를 이용하세요
    if n == 0:
        return 0
    elif n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)    
    


def primes_up_to_n(n: int) -> int:
    # 1부터 N까지의 정수 중에 소수를 모두 찾아 리스트로 반환하는 함수
    # 리스트 컴프리헨션과 조건문을 이용하세요
    def is_prime(num):
        if num < 2:
           return False
        for i in range (2, int( num / 2 ) + 1):
            if num % i == 0:
                return False
        return True

    return [a for a in range(2, n + 1) if is_prime(a)]    
    


def even_numbers(numbers: list[int]) -> list[int]:
    # 정수 리스트에서 짝수들만 골라 리스트로 반환하는 함수를 만드세요
    # 람다 함수식을 사용하세요
    # return list(filter( ####, #### ))
    isEven = lambda x: x % 2 == 0
    return list(filter(isEven, numbers))