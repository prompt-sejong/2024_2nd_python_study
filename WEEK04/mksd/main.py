from calculator import *

print(sum_numbers(1,2,3,4,5,6,7,8,9,10))      # 1~10 까지의 덧셈 = 55
print(multiply(2,3,4,5,6))         # 2~6까지의 곱셈 = 6! = 720
print(factorial(5))             # 5! = 120
print(fibonacci(10))            # 피보나치 10 = 55
print(primes_up_to_n(20))       # 2,3,5,7,11,13,17,19

print(even_numbers(x for x in range(1,30))) # 2~29 까지의 짝수 