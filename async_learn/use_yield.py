"""
使用yield来进行协程切换
"""


def f1():
    yield 1
    yield from f2()
    yield 2


def f2():
    yield 3
    yield 4

# f1()是一个生成器
for i in f1():
    print(i)
