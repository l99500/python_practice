import sys
import shutil
import zipfile
from pathlib import Path

"""
1、解压缩压缩文件
2、执行查找和替换行为
3、压缩新文件
注意：
1、只搜索了zip文件中最上层目录的文件
2、命令行执行指令：
python zip_search.py hello.zip hello hi
"""


class ZipReplace:
    def __init__(self, filename, search_string, replace_string):
        self.filename = filename
        self.search_string = search_string
        self.replace_string = replace_string
        self.temp_directory = Path("unzipped-{}".format(filename))

    def zip_find_replace(self):
        self.unzip_files()
        self.find_replace()
        self.zip_files()

    def unzip_files(self):
        self.temp_directory.mkdir()
        with zipfile.ZipFile(self.filename) as zip_:
            zip_.extractall(str(self.temp_directory))

    def find_replace(self):
        for filename in self.temp_directory.iterdir():
            with filename.open() as file:
                contents = file.read()
            contents = contents.replace(self.search_string, self.replace_string)
            with filename.open("w") as file:
                file.write(contents)

    def zip_files(self):
        with zipfile.ZipFile(self.filename, 'w') as file:
            for filename in self.temp_directory.iterdir():
                file.write(str(filename), filename.name)
        shutil.rmtree(str(self.temp_directory))  # 删除缓存目录


if __name__ == "__main__":
    ZipReplace(*sys.argv[1:4]).zip_find_replace()