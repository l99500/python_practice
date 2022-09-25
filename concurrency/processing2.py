
"""
使用Queue进行进程间通信
一个小型的文件搜索系统
"""


def search(paths, query_q, results_q):
    """
    :param paths: 文件的路径
    :param query_q: 请求的队列
    :param results_q: 结果队列
    :return:
    """
    lines = []
    for path in paths:
        with open(path, 'r', encoding='utf-8') as f:
            temp = f.readlines()
        lines.extend(l.strip() for l in temp)
    query = query_q.get()
    while query:
        results_q.put([l for l in lines if query in l])
        query = query_q.get()


if __name__ == "__main__":
    """
    导入语句放在了if语句下，可以防止在某些操作系统中在每个子进程中都被导入。
    """
    from multiprocessing import Process, Queue, cpu_count
    import os
    from pathlib import Path

    # 找到当前文件所在路径
    current_path = os.path.dirname(os.path.abspath(__file__))

    cpus = cpu_count()
    path_names = [current_path + '/' + f for f in os.listdir(current_path)
                  if Path(current_path + '/' + f).is_file()]
    paths = [path_names[i::cpus] for i in range(cpus)]  # steps 为cpus
    query_queues = [Queue() for p in range(cpus)]
    results_queue = Queue()
    search_process = [
        Process(target=search, args=(p, q, results_queue))
        for p, q in zip(paths, query_queues)
    ]
    for proc in search_process:
        proc.start()

    for q in query_queues:
        q.put("def")
        q.put(None)  # 发送终止信号

    for i in range(cpus):
        for math in results_queue.get():
            print(math)

    for proc in search_process:
        proc.join()
