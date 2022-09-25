import random
from multiprocessing.pool import Pool

"""
计算随机数的质因子
map方法接受一个函数和一个可迭代对象为参数。进程池解包出可迭代对象中的每一个值
并传递给一个可用的进程。
"""


def prime_factor(value):
    factors = []
    for divisor in range(2, value-1):
        # python divmod() 函数把除数和余数运算结果结合起来，返回一个包含商和余数的元组(a // b, a % b)。
        quotient, remainder = divmod(value, divisor)
        if not remainder:
            factors.extend(prime_factor(divisor))
            factors.extend(prime_factor(quotient))
            break
        else:
            factors = [value]
    return factors


if __name__ == '__main__':
    pool = Pool()

    to_factor = [
        random.randint(100000, 50000000) for i in range(20)
    ]
    results = pool.map(prime_factor, to_factor)
    for value, factors in zip(to_factor, results):
        print("The factors of {} are {}".format(value, factors))
