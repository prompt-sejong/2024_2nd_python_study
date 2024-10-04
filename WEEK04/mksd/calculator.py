'''
TODO: 
1. 각 함수명에 걸맞는 연산을 수행하는 함수를 완성하세요.
2. WEEK04.ipynb 에서 import calculator로 함수를 불러와 검증하는 부분을 추가하세요.
3. 모듈 함수 사용방법은 calculator.sum_numbers(1, 2, 3) 식으로 사용할 수 있습니다.
'''


def sum_numbers(*list_num):
    # 복수 개의 정수 입력을 받아 모두 더한 값을 출력하는 함수
    sum = 0
    for num in list_num:
        sum += num
    return sum


def multiply(*list_num):
    # 복수 개의 정수 입력을 받아 모두 곱한 값을 출력하는 함수
    mul = 1
    for num in list_num:
        mul *= int(num)
    return mul


def factorial(n):
    # n이 0 이상일 때, n! 을 반환하는 함수
    # while 문을 사용하세요
    if(n == 0):   
        return 1
    mul = 1
    while(n):       # n ~ 1 까지의 곱셈
        mul *= n
        n -= 1
    return mul

def fibonacci(n):
    # n 번째 피보나치 수를 반환하는 함수
    # 조건문과 재귀함수를 이용하세요
    if(n==1 or n==2):
        return 1
    return fibonacci(n-1)+fibonacci(n-2)


def primes_up_to_n(n):
    # 1부터 N까지의 정수 중에 소수를 모두 찾아 리스트로 반환하는 함수
    # 리스트 컴프리헨션과 조건문을 이용하세요
    dist = [1]*(n+1)
    for i in range(2, int(n**0.5)+1):     # 에라토스테네스의 체 (n의 제곱근까지만 판별해도 소수인지 알 수 있음)
        if dist[i]:
            for j in range(2*i, n+1, i):    # i 가 소수인 경우(=> dist[i] == 1), i의 곱셈을 전부 0으로 만듦
                dist[j] = 0

    return [x for x in range(2,n+1) if dist[x]]


def even_numbers(numbers):
    # 정수 리스트에서 짝수들만 골라 리스트로 반환하는 함수를 만드세요
    # 람다 함수식을 사용하세요
    # return list(filter( ####, #### ))
    return list(filter(lambda x: x%2 == 0, numbers))


# 1. import calculator 
# 2. from calculator import *   의 차이를 확인하는 변수
TEST = 2101                     # 1번은 main.py에서 감지하지 못하고 2번은 가능함
# print(__name__)    
