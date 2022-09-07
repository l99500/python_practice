import unittest
import sys
from collections import defaultdict

######################################


class CheckNumbers(unittest.TestCase):
    def test_int_float(self):
        self.assertEqual(1, 1.0)

    def test_str_float(self):
        self.assertEqual(1, "1")
#####################################


def average(seq):
    return sum(seq) / len(seq)


class TestAverage(unittest.TestCase):
    def test_zero(self):
        self.assertRaises(ZeroDivisionError, average, [])

    def test_with_zero(self):
        with self.assertRaises(ZeroDivisionError):
            # 确保调用某个函数会抛出一个特定的异常，然后通过测试，否则会失败
            average([])
#######################################


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
            return (self[idx] + self[idx-1]) / 2

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


class TestValidInputs(unittest.TestCase):
    def setUp(self) -> None:
        """每次测试前单独调用（重置）， 一向测试不应收到其它测试的影响"""
        self.stats = StatsList([1, 2, 2, 3, 3, 4])

    def test_mean(self):
        self.assertEqual(self.stats.mean(), 2.5)

    def test_median(self):
        self.assertEqual(self.stats.median(), 2.5)
        self.stats.append(4)
        self.assertEqual(self.stats.median(), 3)

    def test_mode(self):
        self.assertEqual(self.stats.mode(), [2, 3])
        self.stats.remove(2)
        self.assertEqual(self.stats.mode(), [3])
#########################################################


class SkipTests(unittest.TestCase):
    @unittest.expectedFailure
    def test_fails(self):
        """意料之中的失败"""
        self.assertEqual(False, True)

    @unittest.skip("Test is useless")
    def test_skip(self):
        """跳过这个测试"""
        self.assertEqual(False, True)

    @unittest.skipIf(sys.version_info.minor == 8, "broken on 3.8")
    def test_skipif(self):
        """如果python版本是3.8则不进行测试"""
        self.assertEqual(False, True)

    @unittest.skipUnless(sys.platform.startswith('linux'), "broken unless on linux")
    def test_skipunless(self):
        """对非linux系统不进行测试"""
        self.assertEqual(False, True)
##############################################################


if __name__ == '__main__':
    unittest.main()