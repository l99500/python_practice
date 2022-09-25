import sys
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from PIL import Image
from bitarray import bitarray
from pathlib import Path

"""
使用行程长度压缩算法来对黑白图片进行压缩。
例如：000011000 可以压缩为 04 12 03
代码中将每一排分为127的组块，因为127个相同的值可以用7位来编码
"""


def compress_chunk(chunk):
    """
    compress_chunk是bitarray这个类的实例
    bitarray的主要优势在于，当在不同进程间打包时，可以占据布尔型或者字节字符串的0、1列表的第8位空间。
    因此其速度更快一些。
    此函数实现了行程长度压缩算法
    """
    # 由字节对象组成的列表（每个字节包括8个0或1）
    compressed = bytearray()
    count = 1
    # 表示当前位 取值为0或者1
    last = chunk[0]
    for bit in chunk[1:]:
        if bit != last:
            # | 按位或运算符：只要对应的二个二进位有一个为1时，结果位就为1。
            # 碰到一个新的数字时讲原来的数据存入一个数组中，第一位为last数值，
            # 后7位为
            compressed.append(count | (128 * last))
            count = 0
            last = bit
        count += 1
    compressed.append(count | (128 * last))
    return compressed


def compress_row(row):
    """压缩图像中一行数据"""
    compressed = bytearray()
    chunks = split_bits(row, 127)
    for chunk in chunks:
        compressed.extend(compress_chunk(chunk))
    return compressed


def split_bits(bits, width):
    """对输入数据进行等长切割"""
    for i in range(0, len(bits), width):
        yield bits[i: i + width]


def compress_in_executor(executor, bits, width):
    row_compressors = []
    # 对图片进行行分割
    for row in split_bits(bits, width):
        compressor = executor.submit(compress_row, row)
        row_compressors.append(compressor)
    compressed = bytearray()
    for compressor in row_compressors:
        compressed.extend(compressor.result())
    return compressed


def compress_image(in_filename, out_filename, executor=None):
    executor = executor if executor else ProcessPoolExecutor()
    table = [0 if i < 200 else 1 for i in range(256)]
    with Image.open(in_filename) as image:
        # 将图片转换为黑白模式，get_data返回一个这些值的迭代器
        bits = bitarray(image.convert('1').point(table, '1').getdata())
        width, height = image.size

    compressed = compress_in_executor(executor, bits, width)

    # 先写入图片的高和宽，再写入压缩后的数据
    with open(out_filename, 'wb') as file:
        file.write(width.to_bytes(2, 'little'))
        file.write(height.to_bytes(2, 'little'))
        file.write(compressed)


def single_image_main(in_filename, out_filename):
    # in_filename, out_filename = sys.argv[1:3]
    # executor = ThreadPoolExecutor(4)
    executor = ProcessPoolExecutor()
    compress_image(in_filename, out_filename, executor)


def compress_dir(in_dir, out_dir):
    """处理每一张图片在一个不同的进程中"""
    if not out_dir.exists():
        out_dir.mkdir()

    executor = ProcessPoolExecutor()
    for file in (f for f in in_dir.iterdir() if f.suffix == '.bmp'):
        out_file = out_dir / (str(file.name)[:-4] + '.rle')
        executor.submit(compress_image, str(file), str(out_file))


def dir_images_main(in_dir, out_dir):
    compress_dir(in_dir, out_dir)


if __name__ == "__main__":
    input_dir = Path("D:/practice/sanic/concurrency/picture")
    output_dir = Path("D:/practice/sanic/concurrency/picture/result")
    # single_image_main(input_dir, output_dir)
    dir_images_main(input_dir, output_dir)
