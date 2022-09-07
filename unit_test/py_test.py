"""
运行指令：
py.test filename -s
"""


class TestNumbers:
    def test_int_float(self):
        assert 1 == 1.0

    def test_int_str(self):
        assert 1 == '1'


#################################################
"""
基于类的测试
运行指令： py.test filename -s
"""


def setup_module(module):
    print("setting up MODULE {0}".format(module.__name__))


def teardown_module(module):
    print("tearing down MODULE {0}".format(module.__name__))


def test_a_function():
    print("RUNNING TEST FUNCTION")


class BaseTest:
    def setup_class(cls):
        print("setting up CLASS {0}".format(cls.__name__))

    def teardown_class(cls):
        print("tearing down CLASS {0}\n".format(cls.__name__))

    def setup_method(self, method):
        print("setting up METHOD {0}".format(method.__name__))

    def teardown_method(self, method):
        print("tearing down METHOD {0}".format(method.__name__))


class TestClass1(BaseTest):
    def test_method_1(self):
        print("RUNNING METHOD 1-1")

    def test_method_2(self):
        print("RUNNING METHOD 1-2")


class TestClass2(BaseTest):
    def test_method_1(self):
        print("RUNNING METHOD 2-1")

    def test_method_2(self):
        print("RUNNING METHOD 2-2")


##############################################################

"""
fnncarg: 函数参数，可以提前定义在测试配置文件中，将配置文件与测试区分开
"""
from collections import defaultdict


class StatsList(list):
    def mean(self):
        """均值"""
        return sum(self) / len(self)

    def median(self):
        """中位数"""
        if len(self) % 2:
            return self[int(len(self) / 2)]
        else:
            idx = int(len(self) / 2)
            return (self[idx] + self[idx - 1]) / 2

    def mode(self):
        """找出出现频率最高的元素"""
        freqs = defaultdict(int)  # 给每一个键一个默认的value，int默认为0
        for item in self:
            freqs[item] += 1
        mode_freq = max(freqs.values())
        modes = []
        for item, value in freqs.items():
            if value == mode_freq:
                modes.append(item)
        return modes

