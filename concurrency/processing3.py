from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from os.path import sep as pathsep
from collections import deque

"""
实现并行的广度优先搜索：
将所有当前目录的子目录添加到队列中，然后是所有这些目录的子目录
"""


def find_files(path, query_string):
    sub_dirs = []
    for p in path.iterdir():
        full_path = str(p.absolute())
        if p.is_dir() and not p.is_symlink():
            sub_dirs.append(p)
        if query_string in full_path:
            print(full_path)

    return sub_dirs


query = '.py'
futures = deque()
# 指向文件系统的根目录，unix系统中是/，windows系统中是C:\
base_dir = Path(pathsep).absolute()


# 使用with，在结束时可以自动清理并关闭所有线程
# max_workers: 同时允许执行多少个线程
with ThreadPoolExecutor(max_workers=10) as executor:
    futures.append(
        executor.submit(find_files, base_dir, query)
    )
    while futures:
        future = futures.popleft()
        if future.exception():
            continue
        elif future.done():
            sub_dirs = future.result()
            for sub_dir in sub_dirs:
                futures.append(executor.submit(find_files, sub_dir, query))
        else:
            futures.append(future)