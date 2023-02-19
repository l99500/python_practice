import gevent

"""
gevent内部基于greenlet，遇到io自动切换
猴子补丁： from gevent import monkey; monkey.patch_all()
"""


def f1():
    print(1)
    gevent.sleep(2)     # 注意不能使用time.sleep(2)，可以使用猴子不定来进行避免。
    print(2)


def f2():
    print(3)
    gevent.sleep(2)
    print(4)


g1 = gevent.spawn(f1)
g2 = gevent.spawn(f2)

# 程序会在这个地方停住，等待g1和g2执行结束再往下执行
gevent.joinall([g1, g2])
