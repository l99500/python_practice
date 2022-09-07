import tempfile
import shutil
import os.path

import pytest

"""
request对象还提供针对函数参数的清理方法，或者在不同测试过程中重复使用的方法，
以及完成在特定范围内进行设置和清理的任务。
执行指令：py.test filename -s
pytest_2.3已经不支持这种定义方法，需要加入
@pytest.fixture(scope="function")
"""


@pytest.fixture(scope="function")
def temp_dir(request):
    dir_ = tempfile.mkdtemp()   # 创建一个临时的文件夹
    print(dir_)

    def cleanup():
        shutil.rmtree(dir_)     # 递归地删除目录以及其内部所有内容

    # 接受一个回调函数在每个使用该函数参数的测试结束之后执行清理任务
    # 此处是清理文件，还可以关闭连接，清空列表或重置队列
    request.addfinalizer(cleanup)
    return dir_


def test_osfiles(temp_dir):
    os.mkdir(os.path.join(temp_dir, 'a'))
    os.mkdir(os.path.join(temp_dir, 'b'))
    dir_contents = os.listdir(temp_dir)
    print("hello")
    assert len(dir_contents) == 2
    assert 'a' in dir_contents
    assert 'b' in dir_contents

