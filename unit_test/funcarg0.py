from collections import defaultdict

import pytest

"""
执行指令：py.tesst filename
pytest_2.3已经不支持这种定义方法，需要加入
@pytest.fixture(scope="function")
"""


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


@pytest.fixture(scope="function")
def valid_stats(request):
    return StatsList([1, 2, 2, 3, 3, 4])


def test_mean(valid_stats):
    assert valid_stats.mean() == 2.5


def test_median(valid_stats):
    assert valid_stats.median() == 2.5
    valid_stats.append(4)
    assert valid_stats.median() == 3


def test_mode(valid_stats):
    assert valid_stats.mode() == [2, 3]
    valid_stats.remove(2)
    assert valid_stats.mode() == [3]
