import time

"""
装饰器模式：
将提供核心功能的对象包裹起来，以修改其功能。被修改对象应该像未被修饰一样进行交互。
用途：（1）增强一个组件响应，因为它需要将数据传送给另一个组件；
（2）支持多种可选操作。
"""


def log_calls(func):
    """接受一个函数返回一个新的函数对象"""
    def wrapper(*args, **kwargs):
        now = time.time()
        print("Calling {0} with {1} and {2}".format(func.__name__, args, kwargs))
        return_value = func(*args, **kwargs)
        print("Executed {0} in {1}ms".format(
            func.__name__, time.time() - now))
        return return_value
    return wrapper


def test1(a, b, c):
    print("\ttest1 called")


def test2(a, b):
    print("\ttest2 called")


def test3(a, b):
    print("\ttest3 called")
    time.sleep(1)


test1 = log_calls(test1)
test2 = log_calls(test2)
test3 = log_calls(test3)

test1(1, 2, 3)
test2(4, b=5)
test3(6, 7)
