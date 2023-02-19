from greenlet import greenlet

"""
使用第三方包手动实现代码块之间的切换
"""


def f1():
    print(1)
    gr2.switch()    # 切换到f2
    print(2)
    gr2.switch()


def f2():
    print(3)
    gr1.switch()
    print(4)


gr1 = greenlet(f1)
gr2 = greenlet(f2)

gr1.switch()