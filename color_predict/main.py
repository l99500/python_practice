import csv
import math
from random import random
from collections import Counter

dataset_filename = 'colors.csv'


def load_colors(filename):
    """利用生成器读取数据集"""
    with open(filename) as dataset_file:
        # 返回文件中所有行的一个迭代器
        lines = csv.reader(dataset_file)
        for line in lines:
            yield tuple(float(y) for y in line[0:3]), line[3]


def generate_colors(count=100):
    """利用random函数生成随机的rgb颜色"""
    for i in range(count):
        # random()随机生成一个[0,1)范围内的实数
        yield random(), random(), random()


def color_distance(color1, color2):
    """计算两个颜色之间的欧氏距离"""
    channels = zip(color1, color2)
    sum_distance_squared = 0
    for c1, c2 in channels:
        sum_distance_squared += (c1 - c2) ** 2
    return math.sqrt(sum_distance_squared)


def nearest_neighbors(model_colors_, num_neighbors):
    """最近邻算法，找到k个与新数据最近的样本取样本中最多的一个类别作为新数据的类别"""
    model = list(model_colors_)
    # 协程，等待外部输入一个rgb色彩元组，用于启动加初始化
    target = yield
    while True:
        # 计算目标颜色与已有颜色之间的欧式距离，并进行排序
        distances_ = sorted(
            ((color_distance(c[0], target), c) for c in model),
        )

        # 协程 等待外部输入，同时输出前k个距离最近的样本
        target = yield [
            d_[1] for d_ in distances_[0: num_neighbors]
        ]


def write_results(filename='output.csv'):
    """将结果输出到文件"""
    with open(filename, "w") as file:
        writer = csv.writer(file)
        while True:
            # 接受send方法发送的内容
            # print("next in here")
            color_, name = yield
            writer.writerow(list(color_) + [name])


def name_colors(get_neighbors_):
    """接受另一个协程作为输入，将传入的值交给输入的协程来进行处理
    然后获取最常见(出现次数最多的类别)的颜色。"""
    color_ = yield
    while True:
        near = get_neighbors_.send(color_)
        name_guess = Counter(
            n[1] for n in near
        ).most_common(1)[0][0]
        color_ = yield name_guess


def process_colors(dataset_filename_="colors.csv"):
    """整体的处理流程"""
    model_colors = load_colors(dataset_filename)
    get_neighbors = nearest_neighbors(model_colors, 5)
    get_color_name = name_colors(get_neighbors)
    output = write_results()

    next(output)
    next(get_neighbors)
    next(get_color_name)

    for color in generate_colors():
        name = get_color_name.send(color)
        output.send((color, name))


if __name__ == "__main__":
    # 测试最近邻
    # model_colors = load_colors(dataset_filename)
    # target_colors = generate_colors(3)
    # get_neighbors = nearest_neighbors(model_colors, 5)
    # next(get_neighbors)
    #
    # for color in target_colors:
    #     distances = get_neighbors.send(color)
    #     print(color)
    #     for d in distances:
    #         print(color_distance(color, d[0]), d[1])

    # 测试输出写文件
    # results = write_results()
    # next(results)
    # for i in range(3):
    #     print(i)
    #     results.send(((i, i, i), i * 10))

    process_colors()